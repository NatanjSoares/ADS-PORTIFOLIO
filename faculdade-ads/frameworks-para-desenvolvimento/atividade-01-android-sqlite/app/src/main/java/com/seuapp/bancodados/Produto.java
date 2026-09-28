package com.seuapp.bancodados;

public class Produto {
    private int id;
    private String nome;
    private double preco;

    public Produto(int id, String nome, double preco) {
        this.id = id;
        this.nome = nome;
        this.preco = preco;
    }

    // Getters
    public int getId() { return id; }
    public String getNome() { return nome; }
    public double getPreco() { return preco; }
}

