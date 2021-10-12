package com.huawei.gauss.yat.setting

object Version {
    private const val YAT_VERSION_MARK = "project ':yat:setting'.version";
    private const val YAT_BUILD_TIME_MARK = "2021-09-27 11:57:03";

    fun detailVersionInfo(): String {
        return "Version $YAT_VERSION_MARK Build At $YAT_BUILD_TIME_MARK"
    }
}