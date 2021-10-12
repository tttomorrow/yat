-- @testpoint: array_agg超过范围测试，合理报错
SELECT char_length(to_char(array_agg(lpad('9',131072,'9')::numeric)::text));
select array_agg(lpad('9',131072,'9')::numeric+1);