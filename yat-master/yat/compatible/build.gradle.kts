plugins {
    kotlin("jvm")
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
}


tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }
}
