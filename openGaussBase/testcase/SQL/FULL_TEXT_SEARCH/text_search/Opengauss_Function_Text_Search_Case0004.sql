--  @testpoint:to_tsquery函数测试（无效性测试）
--检索条件包含！=，合理报错
 SELECT to_tsquery('The != Fat & Rats');
 --检索条件，不添加运算符，报错
 SELECT to_tsquery('Fat Rats');
 --检索条件，由{}括号组成，报错
 SELECT to_tsquery {'english', 'The & Fat & Rats'};
 --检索条件，不添加括号，报错
 SELECT to_tsquery 'english', 'The | Fat | Rats';
 --权重E,报错
 SELECT to_tsquery('supern:*E & star:A*B');
