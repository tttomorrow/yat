--  @testpoint:cursor声明游标，使用value子句，子句类型为字符类型；


start transaction;
cursor cursor21 for values(char 'char',varchar(10) 'cursor test',cast('type clob' as clob),text 'type text');
fetch from cursor21;
close cursor21;
end;
