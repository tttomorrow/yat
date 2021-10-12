plugins {
    kotlin("jvm")
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    implementation("io.github.java-diff-utils:java-diff-utils:4.10")
    implementation(project(":yat:common"))
}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }
}

