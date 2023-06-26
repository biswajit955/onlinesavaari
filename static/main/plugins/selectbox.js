jQuery.fn.extend({
    IconSelectBox: function (img) {

        var defaultSelect = '#' + this.prop('id');
        var optionArray = [];
        // convert id to class if id given as selector
        var prefix_class = defaultSelect.replace('#', '.');

        var createElements = function () {
            var btn_select = extractText(defaultSelect);

            var button = document.createElement('button');
            button.classList = btn_select + '-select-box';

            var div = document.createElement('div');
            div.classList = btn_select + '-b';

            var ul = document.createElement('ul');
            ul.classList = btn_select + '-a';

            $(div).append(ul);

            $(button).insertAfter(defaultSelect);

            $(div).insertAfter(button);
        };

        var getStorage = function () {
            var lastSelected = localStorage.getItem(extractText(prefix_class) + '-curr');

            if (lastSelected) {
                //find an item with value of lastSelected

                $(prefix_class + '-select-box').html(lastSelected + ' <i data-arrow="true" class="fa fa-angle-down"></i>');
                var val = $(prefix_class + '-select-box').find('[data-value]').data('value');

                $(defaultSelect).val(val);
            } else {
                $(prefix_class + '-select-box').html(optionArray[0] + ' <i data-arrow="true" class="fa fa-angle-down"></i>');
                var val = $(optionArray[0]).find('[data-value]').data('value');

                $(defaultSelect).val(val);
            }
        };

        var extractText = function () {
            return defaultSelect.indexOf('#') > -1 ? defaultSelect.replace('#', '') : defaultSelect.replace('.', '');
        };

        var addCss = function () {
            const head = document.querySelector('head');
            const css = prefix_class + '-a {' +
                'padding-left: 0px;' +
                'margin-bottom: 0px;' +
                '}' +

                prefix_class + '-a img, ' + prefix_class + '-select-box img{' +
                'width: 20px;' +
                '}' +

                prefix_class + '-a li{' +
                'list-style: none;' +
                'padding: 6px;' +
                '}' +

                prefix_class + '-a li:hover{' +
                'background-color: #F4F3F3;' +
                '}' +

                prefix_class + '-a li span, ' + prefix_class + '-select-box li span {' +
                'margin-left: 4px;' +
                'font-size: 14px;' +
                '}' +

                prefix_class + '-b {' +
                'margin-top: 2px;' +
                'background-color: #fff;' +
                'position: absolute;' +
                'display: none;' +
                'width: 100%;' +
                'border: 1px solid rgba(0, 0, 0, 0.05);' +
                'border-radius: 4px;' +
                'box-shadow: 0px 2px 4px 1px rgba(0, 0, 0, 0.05);' +
                'overflow: hidden;' +
                'z-index: 9999;' +
                '}' +

                prefix_class + '-select-box {' +
                'display: flex;' +
                'align-items: center;' +
                'position: relative;' +
                'width: 100%;' +
                'background-color: #fff;' +
                'border: 1px solid #fff;' +
                'border-radius: 4px;' +
                'padding: 6px;' +
                '}' +

                prefix_class + '-select-box i {' +
                'top: 10%;' +
                'position: relative;' +
                '}' +

                prefix_class + '-select-box li i {' +
                'font-size: 14px;' +
                '}' +

                prefix_class + '-select-box li {' +
                'display: flex;' +
                'align-items: center;' +
                'list-style: none;' +
                'float: left;' +
                'padding-bottom: 0px;' +
                'width: 95%;' +
                'text-align: left;' +
                '}' +

                prefix_class + '-select-box li {' +
                'line-height: 20px;' +
                'color: #132239;' +
                'cursor: pointer;' +
                '}' +

                prefix_class + '-select-box:hover li {' +
                'margin-left: 0px;' +
                '}' +

                prefix_class + '-select-box:hover {' +
                'background-color: #e4e4e4;' +
                'border: 1px solid transparent;' +
                '}' +

                prefix_class + '-select-box:focus {' +
                'outline:none;' +
                '}';


            $(head).append('<style> ' + css + ' </style>');

        };

        $(defaultSelect).hide();

        $(defaultSelect + ' option').each(function () {
            var text = this.innerText;
            var value = this.value;
            var icon = $(this).data("icon");

            var iconEl = img ? '<img src="' + icon +
                '" alt="icon" data-value="' + value + '"/>' :
                '<i class="' + icon +
                '" data-value="' + value + '"></i>';

            var item = '<li>' + iconEl + ' <span>' + text + '</span></li>';
            optionArray.push(item);
        })

        createElements();
        addCss();

        //console.log(optionArray);
        $(prefix_class + '-a').html(optionArray);

        getStorage();

        //change button stuff on click
        $(prefix_class + '-a li').click(function () {
            var icon = img ? $(this).find('img').attr("src") : $(this).find('i').attr("class");
            var value = img ? $(this).find('img').data('value') : $(this).find('i').data('value');
            var text = this.innerText;

            var iconEl = img ? '<img src="' + icon +
                '" alt="icon" data-value="' + value + '"/>' :
                '<i class="' + icon +
                '" data-value="' + value + '"></i>';

            var item = '<li>' + iconEl + ' <span> ' + text + ' </span>' + '</li>';

            $(prefix_class + '-select-box').html(item + '<i data-arrow="true" class="fa fa-angle-down"></i>');

            $(defaultSelect).val(value);
            $(prefix_class + '-b').toggle();

            localStorage.setItem(extractText(prefix_class) + '-curr', item);
        });

        $(prefix_class + '-select-box').click(function () {
            var cls = $(this).find('[data-arrow]').attr('class');
            if (cls === "fa fa-angle-up") {
                $(this).find('[data-arrow]').attr('class', 'fa fa-angle-down');
            } else {
                $(this).find('[data-arrow]').attr('class', 'fa fa-angle-up');
            }

            $(prefix_class + '-b').toggle();
        });

    }
})