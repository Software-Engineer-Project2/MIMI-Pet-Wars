
         
     function    loadProperties (lang){
            //  var self = this;
            //  var tmp_lang = '';
            //  if(new_lang == 0){
            //      tmp_lang = 'zh';
            //      $('body').removeClass('en').addClass('zh');
            //  }else{
            //      tmp_lang = 'en';
            //      $('body').removeClass('zh').addClass('en');
            //  }
             jQuery.i18n.properties({//加载资浏览器语言对应的资源文件
                 name: 'strings', //资源文件名称
                 path: '../../../static/i18n/', //资源文件路径
                 language: lang,
                 cache: false,
                 mode:'map', //用Map的方式使用资源文件中的值
                 callback: function() {//加载成功后设置显示内容
                     for(var i in $.i18n.map){
                         $('[data-lang="'+i+'"]').text($.i18n.map[i]);
                     }
                     // document.title = $.i18n.map['string_title'];
                 }
             });
            //  self.now_lang = new_lang;
         }
     
     $(document).ready(function(){
        //  loadProperties(now_lang);
        if ($.cookie('lang')=='zh'){
            loadProperties('zh');
        } 
        else{
            loadProperties('en');
        }

         $('#J_lang_switch').click(function(){
            //  var new_lang;
            //  if(now_lang == 0){
            //      new_lang = 1;
            //      now_lang = 1;
            //  }else{
            //      new_lang = 0;
            //      now_lang = 0;
            //  }
            //  loadProperties(new_lang);
            if($.cookie("lang") == 'zh'){
                loadProperties('en');
                $.cookie('lang','en');
            }
            else{
                loadProperties('zh');
                $.cookie('lang','zh');
            }
         });
     });
     