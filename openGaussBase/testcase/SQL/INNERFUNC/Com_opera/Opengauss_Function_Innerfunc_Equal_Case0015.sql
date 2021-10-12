-- @testpoint: opengauss比较操作符=，入参是函数

-- 入参为函数、表达式等
SELECT bit_length('world') = bit_length(right('helloworld',5));
SELECT bit_length(right('helloworld',5)) = bit_length(btrim('sring' , 'ing'));
SELECT char_length('hello') = instr( 'abcdabcdabcd', 'bcd', 2, 2 );
SELECT lpad('hi', 5000, 'xyza') = lpad('hi', 5000, 'xyza');
select 999%3 = 111*1;