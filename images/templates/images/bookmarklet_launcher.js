(function(){

    if (window.myBookmarklet !== undefined){
    
    myBookmarklet();
    
    }
    
    else {
    
    document.body.appendChild(document.createElement('script')).
    
    src='https://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.
    floor(Math.random()*99999999999999999999).addClass("remove");

    //src='https://swiss-social.herokuapp.com/static/js/bookmarklet.js?r='+Math.
    //floor(Math.random()*99999999999999999999).addClass("remove"); //Prodution
    
    }
    
    })();