package com.seuapp.bancodados;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class ProdutoDbHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "produtos.db";
    private static final int DATABASE_VERSION = 1;
    public static final String TABLE_NAME = "produtos";
    public static final String COLUMN_ID = "id";
    public static final String COLUMN_NOME = "nome";
    public static final String COLUMN_PRECO = "preco";

    public ProdutoDbHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        String SQL_CREATE_TABLE = "CREATE TABLE " + TABLE_NAME + " (" +
                COLUMN_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                COLUMN_NOME + " TEXT NOT NULL, " +
                COLUMN_PRECO + " REAL NOT NULL);";
        db.execSQL(SQL_CREATE_TABLE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
        onCreate(db);
    }

    public boolean inserirproduto(String nome, double preco) {
        // Validação básica solicitada pelo roteiro
        if (nome == null || nome.trim().length() < 3 || preco <= 0) {
            return false;
        }

        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues valores = new ContentValues();
        valores.put(COLUMN_NOME, nome);
        valores.put(COLUMN_PRECO, preco);

        long resultado = db.insert(TABLE_NAME, null, valores);
        db.close();
        return resultado != -1;
    }

    public List<String> listarProdutos() {
        List<String> lista = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        String query = "SELECT * FROM " + TABLE_NAME + " ORDER BY " + COLUMN_ID + " DESC";
        Cursor cursor = db.rawQuery(query, null);

        if (cursor.moveToFirst()) {
            do {
                String nome = cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_NOME));
                double preco = cursor.getDouble(cursor.getColumnIndexOrThrow(COLUMN_PRECO));
                lista.add(nome + " - R$ " + String.format(Locale.getDefault(), "%.2f", preco));
            } while (cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return lista;
    }
}