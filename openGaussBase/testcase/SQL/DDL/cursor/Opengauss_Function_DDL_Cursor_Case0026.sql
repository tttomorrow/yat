--  @testpoint:cursor声明游标，使用value子句，子句类型为文本搜索类型；


start transaction;
cursor cursor26 for values('a fat cat sat on a mat and ate a fat rat'::tsvector);
fetch from cursor26;
close cursor26;
end;

