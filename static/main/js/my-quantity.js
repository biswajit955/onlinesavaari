	$(document).ready(function() {
				var name;
				if(document.getElementById("economy").checked){
					name="Economy";
				}else if(document.getElementById("business").checked){
					name="Business";

				}else{
					name="Premimum Economy";
				}

			$('.minus').click(function () {
				var $input = $(this).parent().find('input');
				var count = parseInt($input.val()) - 1;
				count = count < 1 ? 0 : count;
				$input.val(count);

				var data=count.toString().concat(" traveller, ").concat(name);
				$("#countData").text(data);

				$input.change();
				return false;
			});
			$('.plus').click(function () {
				var $input = $(this).parent().find('input');
				$input.val(parseInt($input.val()) + 1);

				var data=(parseInt($input.val()) + 1).toString().concat(" traveller, ").concat(name);
				$("#countData").text(data);

				$input.change();
				return false;
			});
		});

	$(document).ready(function() {
		var name;
				if(document.getElementById("economy").checked){
					name="Economy";
				}else if(document.getElementById("business").checked){
					name="Business";

				}else{
					name="Premimum Economy";
				}
    $('.minus').click(function() {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 0 : count;
        $input.val(count);

		var data=count.toString().concat(" traveller, ").concat(name);
		$("#countData").text(data);

        $input.change();
        return false;
    });
    $('.plus').click(function() {
        var $input = $(this).parent().find('input');


        if ($input.val() < 9) {
            $input.val(parseInt($input.val()) + 1);

			var data=(parseInt($input.val()) + 1).toString().concat(" traveller, ").concat(name);
			$("#countData").text(data);

            $input.change();
            return false;
        }

    });
});


