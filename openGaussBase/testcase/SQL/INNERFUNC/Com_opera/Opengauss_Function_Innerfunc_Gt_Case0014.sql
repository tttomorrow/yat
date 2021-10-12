-- @testpoint: opengauss比较操作符>=，入参为函数
-- 入参为函数
SELECT bit_length('world') >= bit_length('hello world');
SELECT bit_length(right('helloworld',5)) >= bit_length(btrim('sring' , 'ing'));
SELECT char_length('hello') >= instr( 'abcdabcdabcd', 'bcd', 2, 2 );
SELECT lpad('hi', 5, 'xyza') >= lpad('hi', 5000, 'xyza');