-- @testpoint: 函数slice_array(hstore, text[])，提取hstore的值的集合

select slice_array('a=>1,b=>2,c=>3'::hstore, array['b','c','x']);
