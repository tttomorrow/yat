
--问题现象：
--step1建立分区表；执行step3建立全局索引；执行step4查看表结构，发现表结构中主键部分不正常；
--执行step5执行insert语句，数据库core；然而，如果在step1之后执行了step2查看表结果，则step4、step5结果是正常的
--回归测试：
--在step1之后不执行step2，看看step4和step5是否正常

drop table if exists ppinpltable9;
--step1：创建分区表
CREATE TABLE "ppinpltable9"
(
ppid INTEGER,
"dateDATEdatedate714_0" date NOT NULL,
"ncharacter885_1" nchar (14),
"CLOBCLOBCLOB246_2" clob,
"decimal890_3" decimal,
"booleanbooleanBOOLboolean843_4" boolean,
"smallintSMALLINT518_5" smallint,
"TIMESTAMPtimestamptimestamptimestamp765_6" timestamp,
"CLOBclobCLOBclob534_7" clob,
"DOUBLE328_8" double precision,
"TIMESTAMP357_9" timestamp,
"REAL228_10" real,
"SMALLINTSMALLINTsmallintsmallint745_11" smallint,
"SMALLINT293_12" smallint,
"timetimeTIME882_13" time,
"DECIMAL101_14" decimal (63, 18),
"SMALLINT773_15" smallint,
"SMALLINTsmallint671_16" smallint,
"TEXTtextTEXTtext323_17" text,
"TIMESTAMPtimestampTIMESTAMP732_18" timestamp,
"numericNUMERICnumeric490_19" numeric,
"money426_20" money,
"date441_21" date,
"BIGINTbigintBIGINT621_23" bigint,
"TEXTtexttexttext271_24" text,
"SMALLINTsmallint174_25" smallint,
"smallint512_26" smallint,
"smallint745_27" smallint,
"textTEXTTEXT244_28" text,
"realREALREALREAL684_29" real,
"MONEYMONEYMONEYMONEY871_30" money,
"texttexttexttext872_31" text,
PRIMARY KEY ("decimal890_3", ppid)
)
partition by range ("decimal890_3")
(
partition ppinpltable9_p07 values less than (MAXVALUE)
);
--step2：查询表结构
--\d ppinpltable9
--step3: 创建全局索引
CREATE INDEX "ppinpltable9_idx3628" ON "ppinpltable9" ("dateDATEdatedate714_0" DESC NULLS FIRST, "decimal890_3") GLOBAL;
CREATE INDEX "ppinpltable9_idx7163" ON "ppinpltable9" ("dateDATEdatedate714_0" NULLS FIRST, "decimal890_3") GLOBAL;
--step4：查询表结构
--\d ppinpltable9
select indkey from pg_index where indexrelid = (select oid from pg_class where relname = (SELECT conname FROM pg_constraint INNER JOIN pg_class ON pg_constraint.conrelid = pg_class.oid WHERE pg_class.relname = 'ppinpltable9' AND pg_constraint.contype = 'p'));
--step5：执行insert语句
insert into ppinpltable9(ppid, "dateDATEdatedate714_0", "decimal890_3") values(1, '2020-4-22', 3);
--step6：清理表
drop table if exists ppinpltable9;
