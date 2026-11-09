import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-lista-produtos',
  standalone: false,
  styleUrl: './lista-produtos.css',
  templateUrl: './lista-produtos.html',
})
export class ListaProdutos implements OnInit {

  produtos: {
    nome: string;
    preco: number;
    descricao: string;
  }[] = [];

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      const dadosSalvos = localStorage.getItem('produtos');

      if (dadosSalvos) {
        try {
          this.produtos = JSON.parse(dadosSalvos);
        } catch {
          this.produtos = [];
        }
      }
    }
  }
}