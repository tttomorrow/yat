--  @testpoint:函数ts_lexize测试（无效性测试）
--指定字典名为dutch_stem,不支持，合理报错
SELECT ts_lexize('dutch_stem', 'stars');
--指定字典名为finnish_stem,不支持，合理报错
SELECT ts_lexize('finnish_stem', 'stars');
--指定字典名为french_stem,不支持，合理报错
SELECT ts_lexize('french_stem', 'stars');
--指定字典名为german_stem,不支持，合理报错
SELECT ts_lexize('german_stem', 'stars');
--指定字典名为hungarian_stem,不支持，合理报错
SELECT ts_lexize('hungarian_stem', 'stars');
--指定字典名为italian_stem,不支持，合理报错
SELECT ts_lexize('italian_stem', 'stars');
--指定字典名为norwegian_stem,不支持，合理报错
SELECT ts_lexize('norwegian_stem', 'stars');
--指定字典名为portuguese_stem,不支持，合理报错
SELECT ts_lexize('portuguese_stem', 'stars');
--指定字典名为romanian_stem,不支持，合理报错
SELECT ts_lexize('romanian_stem', 'stars');
--指定字典名为russian_stem,不支持，合理报错
SELECT ts_lexize('russian_stem', 'stars');
--指定字典名为spanish_stem,不支持，合理报错
SELECT ts_lexize('spanish_stem', 'stars');
--指定字典名为swedish_stem,不支持，合理报错
SELECT ts_lexize('swedish_stem', 'stars');
--指定字典名为turkish_stem,不支持，合理报错
SELECT ts_lexize('turkish_stem', 'stars');
