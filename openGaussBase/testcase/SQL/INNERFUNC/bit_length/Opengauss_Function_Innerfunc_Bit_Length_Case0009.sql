-- @testpoint: 与concat函数结合使用
 select bit_length(concat('abc',123.00));

 select bit_length(concat('abc',-0.1));