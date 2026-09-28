package com.example.atividade01framework

import android.app.Activity
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.Toast
import com.seuapp.bancodados.ProdutoDbHelper

class MainActivity : Activity() {

    private lateinit var dbHelper: ProdutoDbHelper
    private lateinit var adapter: ArrayAdapter<String>
    private lateinit var listaProdutos: ArrayList<String>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        dbHelper = ProdutoDbHelper(this)

        val etNome = findViewById<EditText>(R.id.etNome)
        val etPreco = findViewById<EditText>(R.id.etPreco)
        val btnSalvar = findViewById<Button>(R.id.btnSalvar)
        val listView = findViewById<ListView>(R.id.listViewProdutos)

        listaProdutos = ArrayList()
        adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, listaProdutos)
        listView.adapter = adapter

        atualizarLista()

        btnSalvar.setOnClickListener {
            val nome = etNome.text.toString()
            val precoTexto = etPreco.text.toString()

            if (nome.trim().length < 3) {
                Toast.makeText(this, "Erro: Nome deve ter no mínimo 3 caracteres.", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val preco = precoTexto.toDoubleOrNull()
            if (preco == null || preco <= 0) {
                Toast.makeText(this, "Erro: Informe um preço válido maior que zero.", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val sucesso = dbHelper.inserirproduto(nome, preco)
            if (sucesso) {
                Toast.makeText(this, "Produto salvo com sucesso!", Toast.LENGTH_SHORT).show()
                etNome.text.clear()
                etPreco.text.clear()
                atualizarLista()
            } else {
                Toast.makeText(this, "Erro ao salvar produto no banco.", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun atualizarLista() {
        listaProdutos.clear()
        listaProdutos.addAll(dbHelper.listarProdutos())
        adapter.notifyDataSetChanged()
    }
}