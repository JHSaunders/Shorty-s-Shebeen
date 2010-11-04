/*
 * jQuery (TY) Drop Down Mega Menu 
 * http://tumharyyaaden.site50.net/
 *
 * Copyright (c) 2009 Ronak Patel 
 * Desisaswat@gmail.com
 * Dual licensed under the MIT and GPL licenses.
 *
 * Date: 2010-05-19 00:00:01 -0500 (Wed, 19 May 2010)
 * Version: 0.1
 */

$(document).ready(function(){

    $(".tiptip").tipTip(); //Initiate tipTip Tooltip, Titles to Tooltip
	
	//Top Navigation Background Animation, inlcude bgpos.js!
	$('#top_navi a') //Top Navigation Background Animation, inlcude bgpos.js!
		.css( {backgroundPosition: "-230px 0"} )
		.mouseover(function(){
			$(this).stop().animate({backgroundPosition:"(0 0)"}, {duration:310});
		})
		.mouseout(function(){
			$(this).stop().animate({backgroundPosition:"(-230px 0)"}, {duration:310});
		});
		
	$('#top_navi .menuboth div a') //Top Navigation, Drop down Links Background Animation, inlcude bgpos.js!
		.css( {backgroundPosition: "-500px -10px"} )
		.mouseover(function(){
			$(this).stop().animate({backgroundPosition:"(0 -10px)", paddingLeft:"21"}, {duration:500});
		})
		.mouseout(function(){
			$(this).stop().animate({backgroundPosition:"(-500px -10px)", paddingLeft:"12"}, {duration:400});
		});
	
	//Drop-Down Menu	
	$('.menuboth').mouseover(function(){
													  
		var containerID = '#'+$('a:first-child', this).attr('menudata'); //Get Menu container ID
		var tall = $('a:first-child', this).attr('menuheight'); //Get Menu container Height
		var wide = $('a:first-child', this).attr('menuwidth'); //Get Menu container Width
		
		$(containerID).stop().animate({height:tall, width:wide}, {queue:false, duration:500, easing:'easeOutBounce'});
	});
	
	//Hide Drop-Down Menu
	$('.menuboth').mouseout(function(){
							  
		var containerID = '#'+$('a:first-child', this).attr('menudata');
		
		$(containerID).stop().animate({height:0,width:0},{queue:false, duration:400, easing: 'easeOutBounce'});
	});

		
	//SearchBox Text Value change function
	var searchfocus = false;		//Set if SearchBox is in focus
	
	$("#searchtxt, #topsearchtxt").click(function(){
		if (this.value=='Search Here...') {
			$(this).val(''); 
			searchfocus = true;		//Don't fade footer if SearchBox is in focus, ignore scroll fade
		}
	})
	.blur(function(){
		if ((this.value==' ')||(this.value=='')) {
			$(this).val("Search Here..."); 
			searchfocus = false; 		//Fade footer if SearchBox is in blur and if page is not scrolled down
			
			var scrollTop = $(window).scrollTop();
			if(scrollTop <= 100) {$('#fixedfooter').stop().animate({'opacity':'0.3'},400);}
		}
		
	});
		
	//Phonebook search URL with variables http://phonebook.uconn.edu/results.php?status=any&basictext=NAME (nonstudent/student)
	$('#phonebtn').click(function(){
		var phoneurl = "http://phonebook.uconn.edu/results.php?status=any&basictext=" + $('#searchtxt').val();
		//window.location.replace(usearchurl); //NO BACK History
		window.location = phoneurl;
	});
	
	$('#topphonebtn').click(function(){
		var phoneurl = "http://phonebook.uconn.edu/results.php?status=any&basictext=" + $('#topsearchtxt').val();
		window.location = phoneurl;
	});
	
	//UConn search URL 
	$('#usearchbtn').click(function (){usearchf();});
	
	function usearchf(){
		var usearchurl = "http://www.uconn.edu/search.php?cx=004595925297557218349%3A65_t0nsuec8&page_id=160&cof=FORID%3A10&ie=UTF-8&&q=" + $('#searchtxt').val();
		window.location = usearchurl;
	}
	
	$('#topusearchbtn').click(function (){topusearchf();});
	
	function topusearchf(){
		var usearchurl = "http://www.uconn.edu/search.php?cx=004595925297557218349%3A65_t0nsuec8&page_id=160&cof=FORID%3A10&ie=UTF-8&&q=" + $('#topsearchtxt').val();
		window.location = usearchurl;
	}
	
});