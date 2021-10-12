--  @testpoint:函数ts_debug测试
--测试一个配置
SELECT * FROM ts_debug('english','a fat  cat sat on a mat - it ate a fat rats');
--省略english
SELECT * FROM ts_debug('a fat  cat sat on a mat - it ate a fat rats');
SELECT ts_debug('english', 'The Brightest supernovaes');
--解析器为pound，解析英文
SELECT ts_debug('pound', 'The Brightest supernovaes');