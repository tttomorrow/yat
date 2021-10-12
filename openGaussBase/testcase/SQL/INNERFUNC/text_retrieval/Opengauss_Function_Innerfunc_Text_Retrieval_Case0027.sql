-- @testpoint: 文本检索操作符&&，@@，结合使用，先将两个tsquery类型的词汇进行“与”操作，词汇类型不一致时返回结果为false

select 'fat cats ate fat rats'::tsvector @@ ('fat'::tsquery  && 'ateee'::tsquery)  as result;
