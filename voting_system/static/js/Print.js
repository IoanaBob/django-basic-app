function Print() {
    this.voter_codes = [];

}   
Print.prototype.add = function(id) {

    if( this.voter_codes.indexOf(id) != -1) {
       
        
        $('#print_total').text( parseInt(parseInt($('#print_total').text()) - 1));
        this.voter_codes.pop(id);

        if(this.voter_codes.length == 0)
            this.destroyGUI();

    } else {
        this.voter_codes.push(id);

        if($('.voter_codes_to_print').length == 0)
            this.createGUI();
       
        $('#print_total').text( parseInt(parseInt($('#print_total').text()) + 1));
    }
    
    
   
}
Print.prototype.createGUI = function() {

    if(this.voter_codes.length == 0){
        $('body').append('<div class="popover voter_codes_to_print"  role="tooltip"><div class="popover-arrow"></div><h3 class="popover-title">List of Voter Codes</h3><div class="popover-content"><h3 class="center">Total</h4><span id="print_total" class="totalPrint">0</span></div><button class="btn btn-success" style="width:100%" id="process_printing">Print</button><a href="#" ><button class="btn btn-warning" style="width:100%"id="reload" >Cancel</button></a></div>');
        $('.popover').animate({opacity: 1});
    }
}
Print.prototype.destroyGUI = function() {

    $('.voter_codes_to_print.popover').animate({opacity: 0});
     $('.voter_codes_to_print.popover').remove();
}
Print.prototype.randIdentifier = function() {
    char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
    rand = "";
    for( i = 0; i < this.rand_length; i++) rand += char.charAt(Math.floor(Math.random() *  char.length + 1));

    if(this.uids.indexOf(rand) != -1)
        this.randIdentifier();
    else
        return rand;
}
Print.prototype.find = function(key) {
     for(var i=0; i < this.voter_codes.length; i++) {
         console.log(this.voter_codes[i])
        if(this.voter_codes[i].hasOwnProperty(key)) {
            return i;
        }
    }
    return -1;
}
Print.prototype.send = function() {
    $.ajax({
        url: "/administration/codes/print/process/",
        type: "post",
        data : {
            "csrfmiddlewaretoken": this.getCookie("csrftoken"),
            'voter_codes': JSON.stringify(this.voter_codes)
        },
        error: function(e) {
            
            console.log(e);
        },
        success: function(e) {
            location.reload();
        }
    })
}
Print.prototype.csrfSafeMethod = function(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
Print.prototype.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}