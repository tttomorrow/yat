/* 
 * Copyright (c) 2021 Huawei Technologies Co.,Ltd.
 *
 * openGauss is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *           http://license.coscl.org.cn/MulanPSL2
 *        
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 */

package com.huawei.gauss.yat.common

import kotlin.collections.ArrayList


class ArrayCycleQueue<T>(capacity: Int): Iterable<T> {
    private val queue: Array<Any?> = arrayOfNulls(capacity)

    private var head = 0
    private var tail = 0

    constructor(init: Collection<T>): this(init.size) {
        init.forEachIndexed { index, it ->
            queue[index] = it
        }
    }

    fun add(ele: T) {
        if (queue[tail] == null) {
            queue[tail] = ele
            tail = (tail + 1) % queue.size
        } else {
            throw QueueFullException()
        }
    }

    fun poll(): T? {
        @Suppress("UNCHECKED_CAST")
        val res = queue[head] as T?

        return if (res == null) {
            null
        } else {
            queue[head] = null
            head = (head + 1) % queue.size
            res
        }
    }

    fun peek(): T? {
        if (size() == 0) {
            throw IndexOutOfBoundsException("size = ${size()}")
        }
        @Suppress("UNCHECKED_CAST")
        return queue[head] as T?
    }

    fun peek(i: Int): T? {
        return if (size() <= i) {
            throw IndexOutOfBoundsException("size = ${size()}, index = $i")
        } else {
            @Suppress("UNCHECKED_CAST")
            queue[(head + i) % queue.size] as T?
        }
    }

    val isEmpty: Boolean
        get() = queue[head] == null

    fun size(): Int {
        return if (queue[tail] != null) {
            queue.size
        } else {
            (tail - head + queue.size) % queue.size
        }
    }

    fun isFull(): Boolean {
        return tail == head && queue[tail] != null
    }

    fun clear() {
        if (size() > 0) {
            var pos = head
            (0 until size()).forEach { _ ->
                queue[pos] = null
                pos = (pos + 1) % queue.size
            }
        }

        tail = 0
        head = 0
    }

    fun read(start: Int = 0, size: Int = -1): ArrayList<T> {
        if (size > size()) {
            throw IndexOutOfBoundsException("given arguments size is bigger than the current size")
        }

        val readSize = if (size == -1) {
            size() - start
        } else {
            size
        }

        val res = ArrayList<T>(readSize)

        var pos = (head + start) % queue.size
        (1..readSize).forEach { _ ->
            @Suppress("UNCHECKED_CAST")
            res.add(queue[pos] as T)
            pos = (pos + 1) % queue.size
        }

        return res
    }

    override fun iterator(): Iterator<T> {
        return QueueIterator()
    }

    inner class QueueIterator: Iterator<T> {
        private var pos = head
        private val size = size()
        private var readed = 0

        override fun hasNext(): Boolean {
            return size > 0 && readed < size
        }

        override fun next(): T {
            val res = queue[pos]
            pos = (pos + 1) % queue.size
            readed++
            @Suppress("UNCHECKED_CAST")
            return res as T
        }
    }
}