void function(){
	function encodeHTML(text){
		return String(text).replace(/["<>& ]/g, function(all){
					return "&" + {
					'"': 'quot',
					'<': 'lt',
					'>': 'gt',
					'&': 'amp',
					' ': 'nbsp'
					}[all] + ";";
					});
	}

	var go = document.getElementById('su');
	var kw = document.getElementById('kw');
	var results = document.getElementById('results');
	kw.focus();
	function search(){
		results.innerHTML = kw.value &&　'\
							<p style="margin:0 15px 10px 0"><b><font class="f14">根据相关法律法规和政策,"' + encodeHTML(kw.value) + '"搜索结果未予显示 （用时 0.0000001 秒）</font></b></p>\
							<p style="margin:20px 15px 10px 0">\
							</p>';
		kw.focus();
	}

	go.onclick = search;
	kw.onkeydown = function(e){
		e = e || event;
		if (e.keyCode == 13) search();
	};
}();
