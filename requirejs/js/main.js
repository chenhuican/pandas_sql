/*
    require.config执行baseUrl为'js'，
    baseUrl指的模块文件的根目录，可以是绝对路径或相对路径
*/
require.config({
		baseUrl: 'js',
		paths: {
			jquery: 'jquery.min'
		}
});
/*
    这里通过require，来引入monkey.js，
    然后通过后面的匿名函数给他们分配参数，如这里的
    monkey-->mk
*/
require(['monkey'],function(mk){
		mk.init();
});

require(['one'],function(one3) {
    alert(one3.key);   
});
