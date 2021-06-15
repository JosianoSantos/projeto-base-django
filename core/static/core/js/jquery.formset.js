/**
 * jQuery Formset 1.3-pre
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Copyright (c) 2009, Stanislaus Madueke
 * All rights reserved.
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */

$(document).ready(function () {
    setTimeout(function () {
        removerLabelFormset();
        aplicarSelect2Formset();
        aplicarMascaras();
        aplicarDatepickerFormset();
    }, 200);

})

;(function ($) {
    $.fn.formset = function (opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts),
            flatExtraClasses = options.extraClasses.join(' '),
            totalForms = $('#id_' + options.prefix + '-TOTAL_FORMS'),
            maxForms = $('#id_' + options.prefix + '-MAX_NUM_FORMS'),
            minForms = $('#id_' + options.prefix + '-MIN_NUM_FORMS'),
            childElementSelector = 'input,select,textarea,label,div',
            $$ = $(this),

            applyExtraClasses = function (row, ndx) {
                if (options.extraClasses) {
                    row.removeClass(flatExtraClasses);
                    row.addClass(options.extraClasses[ndx % options.extraClasses.length]);
                }
            },

            updateElementIndex = function (elem, prefix, ndx) {
                var idRegex = new RegExp(prefix + '-(\\d+|__prefix__)-'),
                    replacement = prefix + '-' + ndx + '-';
                if (elem.attr("for")) elem.attr("for", elem.attr("for").replace(idRegex, replacement));
                if (elem.attr('id')) elem.attr('id', elem.attr('id').replace(idRegex, replacement));
                if (elem.attr('name')) elem.attr('name', elem.attr('name').replace(idRegex, replacement));
            },

            hasChildElements = function (row) {
                return row.find(childElementSelector).length > 0;
            },

            showAddButton = function () {
                return maxForms.length === 0 ||   // For Django versions pre 1.2
                    (maxForms.val() === '' || (maxForms.val() - totalForms.val() > 0));
            },

            /**
             * Indicates whether delete link(s) can be displayed - when total forms > min forms
             */
            showDeleteLinks = function () {
                return minForms.length === 0 ||   // For Django versions pre 1.7
                    (minForms.val() === '' || (totalForms.val() - minForms.val() > 0));
            },

            insertDeleteLink = function (row) {
                var delCssSelector = $.trim(options.deleteCssClass).replace(/\s+/g, '.'),
                    addCssSelector = $.trim(options.addCssClass).replace(/\s+/g, '.');

                // Otherwise, just insert the remove button as the
                // last child element of the form's container:
                row.append('<div class=" formset-delete-div" style="margin-top: 1.4rem">' +
                    '<a id="id_' + options.prefix + '-btn-delete" title="Excluir" data-toggle="tooltip" class="' + options.prefix + '-btn-delete ' + options.deleteCssClass + ' font-15 btn btn-outline-danger btn-sm btn-icon-only mr-0" href="javascript:void(0)">' +
                    '<i class="la la-trash" style="font-size: 23px"></i> ' + options.deleteText + '</a></div>');
                //.children(':nth-last-child(2)')

                // Check if we're under the minimum number of forms - not to display delete link at rendering
                if (!showDeleteLinks()) {
                    row.find('a.' + delCssSelector).hide();
                }

                row.find('a.' + delCssSelector).click(function () {

                    removerLabelFormset();

                    var row = $(this).parents('.' + options.formCssClass),
                        del = row.find('input:hidden[id $= "-DELETE"]'),
                        buttonRow = row.siblings("a." + addCssSelector + ', .' + options.formCssClass + '-add'),
                        forms;
                    if (del.length) {
                        // We're dealing with an inline formset.
                        // Rather than remove this form from the DOM, we'll mark it as deleted
                        // and hide it, then let Django handle the deleting:
                        del.val('on');
                        row.hide();
                        forms = $('.' + options.formCssClass).not(':hidden');
                    } else {
                        row.remove();
                        // Update the TOTAL_FORMS count:
                        forms = $('.' + options.formCssClass).not('.formset-custom-template');
                        totalForms.val(forms.length);
                    }
                    for (var i = 0, formCount = forms.length; i < formCount; i++) {
                        // Apply `extraClasses` to form rows so they're nicely alternating:
                        applyExtraClasses(forms.eq(i), i);
                        if (!del.length) {
                            // Also update names and IDs for all child controls (if this isn't
                            // a delete-able inline formset) so they remain in sequence:
                            forms.eq(i).find(childElementSelector).each(function () {
                                updateElementIndex($(this), options.prefix, i);
                            });
                        }
                    }

                    // Check if we've reached the minimum number of forms - hide all delete link(s)
                    if (!showDeleteLinks()) {
                        $('a.' + delCssSelector).each(function () {
                            $(this).hide();
                        });
                    }
                    // Check if we need to show the add button:
                    if (buttonRow.is(':hidden') && showAddButton()) buttonRow.show();
                    // If a post-delete callback was provided, call it with the deleted form:
                    if (options.removed) options.removed(row);
                    return false;
                });
            };

        removerLabelFormset();

        $$.each(function (i) {
            var row = $(this),
                del = row.find('input:checkbox[id $= "-DELETE"]');
            if (del.length) {
                // If you specify "can_delete = True" when creating an inline formset,
                // Django adds a checkbox to each form in the formset.
                // Replace the default checkbox with a hidden field:
                if (del.is(':checked')) {
                    // If an inline formset containing deleted forms fails validation, make sure
                    // we keep the forms hidden (thanks for the bug report and suggested fix Mike)
                    del.before('<input type="hidden" name="' + del.attr('name') + '" id="' + del.attr('id') + '" value="on" />');
                    row.hide();
                } else {
                    del.before('<input type="hidden" name="' + del.attr('name') + '" id="' + del.attr('id') + '" />');
                }
                // Hide any labels associated with the DELETE checkbox:
                $('label[for="' + del.attr('id') + '"]').hide();
                del.remove();
            }
            if (hasChildElements(row)) {
                row.addClass(options.formCssClass);
                if (row.is(':visible')) {
                    insertDeleteLink(row);
                    applyExtraClasses(row, i);
                }
            }
        });

        if ($$.length) {
            var hideAddButton = !showAddButton(),
                addButton, template;
            if (options.formTemplate) {
                // If a form template was specified, we'll clone it to generate new form instances:
                template = (options.formTemplate instanceof $) ? options.formTemplate : $(options.formTemplate);
                template.removeAttr('id').addClass(options.formCssClass + ' formset-custom-template');
                template.find(childElementSelector).each(function () {
                    updateElementIndex($(this), options.prefix, '__prefix__');
                });
                insertDeleteLink(template);
            } else {
                // Otherwise, use the last form in the formset; this works much better if you've got
                // extra (>= 1) forms (thnaks to justhamade for pointing this out):
                template = $('.' + options.formCssClass + ':last').clone(true).removeAttr('id');
                template.find('input:hidden[id $= "-DELETE"]').remove();
                // Clear all cloned fields, except those the user wants to keep (thanks to brunogola for the suggestion):
                template.find(childElementSelector).not(options.keepFieldValues).each(function () {
                    var elem = $(this);
                    // If this is a checkbox or radiobutton, uncheck it.
                    // This fixes Issue 1, reported by Wilson.Andrew.J:
                    if (elem.is('input:checkbox') || elem.is('input:radio')) {
                        elem.attr('checked', false);
                    } else {
                        elem.val('');
                    }
                });
            }
            // FIXME: Perhaps using $.data would be a better idea?
            options.formTemplate = template;

            // Otherwise, insert it immediately after the last form:
            $$.filter(':last').after('<div class="formset-adicionar-nova-linha-div form-group col-sm-12 mt-0 row">' +
                '<a id="id_' + options.prefix + '-btn-adicionar-nova-linha" class="' +
                options.prefix + '-btn-adicionar-nova-linha ' + options.addCssClass + '  btn btn-secondary " style="font-size: 0.9rem!important;" href="javascript:void(0)">' +
                '<i class="la la-plus"></i> ' + options.addText + '</a></div>');

            addButton = $$.filter(':last').next();
            if (hideAddButton) addButton.hide();

            addButton.click(function () {

                var formCount = parseInt(totalForms.val()),
                    row = options.formTemplate.clone(true).removeClass('formset-custom-template'),
                    buttonRow = $($(this).parents('tr.' + options.formCssClass + '-add').get(0) || this)
                delCssSelector = $.trim(options.deleteCssClass).replace(/\s+/g, '.');
                applyExtraClasses(row, formCount);
                row.insertBefore(buttonRow).show();
                row.find(childElementSelector).each(function () {
                    updateElementIndex($(this), options.prefix, formCount);
                });
                totalForms.val(formCount + 1);
                // Check if we're above the minimum allowed number of forms -> show all delete link(s)
                if (showDeleteLinks()) {
                    $('a.' + delCssSelector).each(function () {
                        $(this).show();
                    });
                }

                removerLabelFormset();

                aplicarSelect2Formset();
                aplicarMascaras();
                aplicarDatepickerFormset();
                // Check if we've exceeded the maximum allowed number of forms:
                if (!showAddButton()) buttonRow.hide();
                // If a post-add callback was supplied, call it with the added form:
                if (options.added) options.added(row);

                return false;
            });

        }

        return $$;
    };

    /* Setup plugin defaults */
    $.fn.formset.defaults = {
        prefix: 'form',                  // The form prefix for your django formset
        formTemplate: null,              // The jQuery selection cloned to generate new form instances
        addText: 'Adicionar nova linha',          // Text for the add link
        deleteText: '',            // Text for the delete link
        addCssClass: 'add-row',          // CSS class applied to the add link
        deleteCssClass: 'delete-row',    // CSS class applied to the delete link
        formCssClass: 'dynamic-form',    // CSS class applied to each form in a formset
        extraClasses: [],                // Additional CSS classes, which will be applied to each form in turn
        keepFieldValues: 'input:checkbox',             // jQuery selector for fields whose values should be kept when the form is cloned
        added: function () {
            // Function called each time a new form is added
        },
        removed: function () {
            // Function called each time a form is deleted
        }
    };
})(jQuery);

function removerLabelFormset() {
    $(`[class*='dynamic']:not(:eq(0)) > div.form-group`).find('label').not('.ui-switch').hide();

    $('.formset-delete-div:not(:eq(0))').css('margin-top','0');
    $('.add-obervacao-div > a:not(:eq(0))').css('margin-top','0');
}