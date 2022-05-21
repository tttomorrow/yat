-- @testpoint: PostGIS功能覆盖,计算geogA的长度,ST_Length

--step1:创建表   expect:成功
drop table if exists t_postgis_0021_01;
drop table if exists t_postgis_0021_02;
drop table if exists t_postgis_0021_03;
create table t_postgis_0021_01(smgeometry1 geometry(MultiPolygon,4490),
                          smgeometry2 geometry(MultiLineString,4490),
                          smgeometry3 geometry(MultiPoint,4490));
create table t_postgis_0021_02(smgeometry1 geometry(Polygon,4490),
                          smgeometry2 geometry(LineString,4490),
                          smgeometry3 geometry(Point,4490));
create table t_postgis_0021_03(length double precision);

--step2:插入数据   expect:成功
insert into t_postgis_0021_01 values(
ST_GeomfromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490),
ST_GeomfromText('MULTILINESTRING((0 0,1 1,1 2),(2 3,3 2,5 4))',4490),
ST_GeomfromText('MULTIPOINT((0 0),(1 2))',4490));
insert into t_postgis_0021_02 values(
ST_GeomfromText('POLYGON((0 0,4 0,4 4,0 4,0 0))',4490),
ST_GeomfromText('LINESTRING(0 0,1 1,1 2)',4490),
ST_GeomfromText('POINT(5 9)',4490));

--step3:结合表查看数据   expect:成功
--计算多点smgeometry3的长度，返回值为0
select ST_Length(smgeometry3) from t_postgis_0021_01;

--计算多线smgeometry2的长度
select ST_Length(smgeometry2) from t_postgis_0021_01;

--计算多面smgeometry1的长度，返回值为0
select ST_Length(smgeometry1) from t_postgis_0021_01;

--计算点smgeometry3的长度，返回值为0
select ST_Length(smgeometry3) from t_postgis_0021_02;

--计算线smgeometry2的长度
select ST_Length(smgeometry2) from t_postgis_0021_02;

--计算面smgeometry1的长度，返回值为0
select ST_Length(smgeometry1) from t_postgis_0021_02;

--将查出来的长度值插入到指定表格的字段中
create or replace procedure p_postgis_0021()
as
sqlstat varchar(200);
begin
    for s1 in select smgeometry2 from t_postgis_0021_01 loop
    sqlstat := 'insert into t_postgis_0021_03(length) values('''||ST_Length(s1.smgeometry2)||''')';
    execute immediate sqlstat;
    end loop;
    for s2 in select smgeometry2 from t_postgis_0021_02 loop
    sqlstat := 'insert into t_postgis_0021_03(length) values('''||ST_Length(s2.smgeometry2)||''')';
    execute immediate sqlstat;
    end loop;
end;
/

call p_postgis_0021();
select length from t_postgis_0021_03;

--step4:清理环境   expect:成功
drop table t_postgis_0021_01 cascade;
drop table t_postgis_0021_02 cascade;
drop procedure p_postgis_0021;
