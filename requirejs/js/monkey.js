/*
    define的参数为匿名函数，该匿名函数返回一个对象
*/
define(['jquery'],function($){
	var init =function(){
		console.log($.browser);
	};
	return {
		init:init
	};
});