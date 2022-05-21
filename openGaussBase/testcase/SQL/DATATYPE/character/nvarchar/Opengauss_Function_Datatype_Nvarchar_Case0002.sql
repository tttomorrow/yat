-- @testpoint: 对NVARCHAR(n)中n的测试 部分测试点合理报错

--step1:执行以下n的无效值; expect:合理报错
select 'aaaaa'::nvarchar(-1);
select 'aaaaa'::nvarchar('a');
select 'aaaaa'::nvarchar();
select 'aaaaa'::nvarchar( );
select 'aaaaa'::nvarchar(' ');
select 'aaaaa'::nvarchar(2.5);
select 'aaaaa'::nvarchar(0);
select 'aaaaa'::nvarchar(*);
select 'aaaaa'::nvarchar(π);
--10*1024*1024+1=10485761
select 'aaaaa'::nvarchar(10485761);

--step2:n>将存值; expect:成功
select 'test'::nvarchar(10);

--step3:n=将存值; expect:成功
select 'test'::nvarchar(4);

--step4:n<将存值; expect:成功,被截取
select 'test'::nvarchar(2);
select 'test'::nvarchar2(2);
