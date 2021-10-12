package com.huawei.gauss.yat.setting

class SettingParseError : RuntimeException {
    constructor(msg: String) : super(msg)
    constructor(e: Throwable) : super(e)
    constructor(msg: String, e: Throwable) : super(msg, e)
}