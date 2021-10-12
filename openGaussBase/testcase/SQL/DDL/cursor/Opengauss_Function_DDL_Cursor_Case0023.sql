--  @testpoint:cursor声明游标，使用value子句，子句类型为日期/时间类型；


start transaction;
cursor cursor23 for values(date '08-12-2020',
                           time without time zone '16:38:22',
                           time with time zone '16:40:40 pst',
                           timestamp without time zone '2020-08-12',
                           timestamp with time zone '2020-08-12 pst',
                           smalldatetime '2020-08-12 16:40:06');

fetch forward 6 from cursor23;
close cursor23;
end;

