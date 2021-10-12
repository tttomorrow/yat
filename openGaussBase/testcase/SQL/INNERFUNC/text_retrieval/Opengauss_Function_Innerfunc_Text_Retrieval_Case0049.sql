-- @testpoint: 文本比较操作符 = ，检查两个tsquery类型的词汇是否相等3

select 'fat'::tsquery  = 'fat'::tsquery as result;