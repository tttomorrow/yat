--  @testpoint:条件表达式，使用decode函数
--返回1
SELECT decode('A','A',1,'B',2,0);
--返回2
SELECT decode('B','A',1,'B',2,0);
--返回0
SELECT decode('C','A',1,'B',2,0);