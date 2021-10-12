-- @testpoint: 删除数组array中所有的anyelement元素，element用函数嵌套结果代替，部分合理报错

--返回类型一致
--函数返回值类型为int,替代element
select array_remove(array[1,2,2,3],(select length('world')));
select array_remove(array[1,2,33,5],(select length('world')));
select array_remove(array[1,2,33,5],(select char_length('hello')));

--函数返回值类型为text,替代element
select array_remove(array['string','str','st','ring'],(select btrim('string' , 'ing')));
select array_remove(array['string','str','st','tri','ring'],(select substrb('string',2,3)));
select array_remove(array['string','str','st','ring'],(select left('abcde', 2)));
select array_remove(array['abcd','str','ababab','abstring'],(select repeat('ab', 3)));

--函数返回值类型为bool，替代element
select array_remove(array[true,false,'1','0','t','f'],(select notlike(1,2)));
select array_remove(array[true,false,'1','0','t','f'],(select notlike(2,2)));

--返回类型不一致
--函数返回值类型为text
select array_remove(array[1,2,2,3],(select btrim('string' , 'ing')));
select array_remove(array[1,2,33,5],(select left('abcde', 2)));
select array_remove(array[1,2,33,5],(select repeat('ab', 3)));

--函数返回值类型为int
select array_remove(array['string','str','st','ring'],(select length('world')));
select array_remove(array['string','str','st','tri','ring'],(select char_length('hello')));
select array_remove(array['string','str','st','ring'],(select length('world')));
select array_remove(array['abcd','str','ababab','abstring'],(select array_ndims(array[[1,2,3], [4,5,6]]) as result));

--函数返回值类型为int和text
select array_remove(array[true,false,'1','0','t','f'],(select length('world')));
select array_remove(array[true,false,'1','0','t','f'],(select left('abcde', 2)));