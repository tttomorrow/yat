--  @testpoint: --update验证字段名大小写敏感
update false_1 set B=0;
update false_1 set b=0;
update false_1 set a=1 where B=0;