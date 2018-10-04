package io.github.romulus10.blckchnmsg.blckchnmsg.data

import java.util.ArrayList
import java.util.HashMap

object Message {

    val ITEMS: MutableList<Message> = ArrayList()

    val ITEM_MAP: MutableMap<String, Message> = HashMap()

    private val COUNT = 25

    private fun addItem(item: Message) {
        ITEMS.add(item)
        ITEM_MAP[item.id] = item
    }

    private fun createMessage(id: String, to: Contact, from: Contact, message: String, signature: String): Message {
        return Message(id, to, from, message, signature)
    }

    data class Message(val id: String, val to: Contact, val from: Contact, val message: String, val signature: String) {
        override fun toString(): String = message
    }
}
