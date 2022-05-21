-- @testpoint: 创建file_fdw外表相关options相关参数校验规则验证，异常情况合理报错，满足条件正常创建

--step1: 创建服务; expect:成功
create server file_server0002 foreign data wrapper file_fdw;
--step2: filename不指定，异常报错; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002;

----format
--step3: format指定非正常格式; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'xml');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'err');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'fixed'  );
--step4: format正常格式不指定filename; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text');
--step5: format正常场景; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'text');
drop foreign table t_filefdw_0002;
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'binary');
drop foreign table t_filefdw_0002;
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'csv');
drop foreign table t_filefdw_0002;

----header
--step6: 指定header，不指定format; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', header 'true');
--step7: 指定header，指定format不符合条件，header为true; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'text', header 'true');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'binary', header 'on');
--step8: 指定header，指定format不符合条件，header为false; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'text', header 'false');
drop foreign table t_filefdw_0002;
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'binary', header 'off');
drop foreign table t_filefdw_0002;
--step9: 指定header不符合条件; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'text', header 'err');
--step10: 指定header，指定format符合条件，header为true; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'csv', header 'true');
drop foreign table t_filefdw_0002;
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'csv', header 'on');
drop foreign table t_filefdw_0002;

----quote
--step11: 指定quote，不指定format; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', quote ':');
--step12: 指定quote非单字节; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', quote ':"');
--step13: 指定quote时与format类型不符; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', quote ':');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'binary', quote ':');
--step14: 指定quote与null参数包含; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', quote '-', null '=-=');
--step15: 指定quote与delimiter参数包含; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', quote '-', delimiter '=-=');
--step16: 指定quote与null参数非包含关系; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'csv', quote '-', null '==');
drop foreign table t_filefdw_0002;
--step17: 指定quote与delimiter参数非包含关系; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'csv', quote '-', null '==');
drop foreign table t_filefdw_0002;

----escape
--step18: 指定escape，不指定format，指定escape; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', escape '"');
--step19: 指定escape，指定format非csv格式; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', escape ':');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'binary', escape ':');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', escape '-');
--step20: 指定escape多字节; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', escape ':"');
--step21: 指定escape、format正确; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'csv', escape ':');
drop foreign table t_filefdw_0002;


--delimiter
--step22: 指定delimiter，不指定format; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', delimiter '');
drop foreign table t_filefdw_0002;
--step23: delimiter超出10个字符; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', delimiter '           ');
--step24: 指定delimiter，delimiter不符合要求; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', delimiter 'a');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', delimiter '8');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', delimiter '\');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'text', delimiter '.');
--step25: delimiter与quote参数相同; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', delimiter '-', quote '-');
--step26: delimiter与quote参数不相同; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '',format 'csv', delimiter '-', quote '`');
drop foreign table t_filefdw_0002;
--step27: delimiter与null参数相同或者包含; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', delimiter '-', null '=-=');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', delimiter '-', null '-');
--step28: delimiter与null参数不相同或者不包含; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', format 'csv', delimiter '-', null '空');
drop foreign table t_filefdw_0002;
--step29: delimiter 为换行符; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', delimiter '
');

----null
--step30: null值指定为换行符; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', null '
');
--step31: null值指定为101个字符串; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (format 'csv', null 'qqweewqqqqqqqqqqqqqqqvxcvxcvxcvxcvqqweewqqqqqcvxcvxcvxcvqqqqqqqqqqvxcvxcvxcvxcvqqqqqqqqqqqvxcvxcvxcvx');
--step32: null值指定为100个字符串; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', null 'qqweewqqqqqqqqqqqqqqqvxcvxcvxcvxcvqqweewqqqqqcvxcvxcvxcvqqqqqqqqqqvxcvxcvxcvxcvqqqqqqqqqqqvxcvxcvxcv');
drop foreign table t_filefdw_0002;

----encoding
--step33: 指定编码格式不正确和为空场景; expect:失败
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', encoding '');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', encoding 'err');
--step34: 指定编码格式正确; expect:成功
create foreign table t_filefdw_0002 (id int) server file_server0002 options (filename '', encoding 'utf-8');
drop foreign table t_filefdw_0002;

----force_not_null
--step35: force_not_null外部对象创建引用; expect:失败
alter foreign data wrapper file_fdw options (add force_not_null '*');
alter server file_server0002 options (add force_not_null '*');
create user mapping for public server file_server0002 options (force_not_null '*');
create foreign table t_filefdw_0002 (id int) server file_server0002 options (force_not_null '*');
--step36：创建外表列使用force_not_nulloption并select外表; expect:创建成功，select失败
create foreign table t_filefdw_0002 (id int options (force_not_null 'true')) server file_server0002 options (filename '');
select * from t_filefdw_0002;
--step37：alter 外表 format 'csv'; expect:成功
alter foreign table t_filefdw_0002 options (add format 'csv');
select * from t_filefdw_0002;
drop foreign table t_filefdw_0002;
--step38：处理测试数据; expect:成功
drop server file_server0002 cascade;