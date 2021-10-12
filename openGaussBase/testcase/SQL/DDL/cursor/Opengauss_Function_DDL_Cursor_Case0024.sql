--  @testpoint:cursor声明游标，使用value子句，子句类型为几何类型；


start transaction;
cursor cursor24 for values(box(circle '((0,0),2.0)'),diameter(circle '((0,0),2.0)'));
fetch from cursor24;
close cursor24;
end;

