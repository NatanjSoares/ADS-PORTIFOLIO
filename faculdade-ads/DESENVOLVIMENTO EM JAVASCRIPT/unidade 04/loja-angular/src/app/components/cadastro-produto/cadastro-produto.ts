import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
@Component({
  selector: 'app-cadastro-produto',
  standalone: false,
  templateUrl: './cadastro-produto.html',
  styleUrl: './cadastro-produto.css',
})
export class CadastroProduto implements OnInit {

  nome: string = '';
  preco: number | null = null;
  descricao: string = '';

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

  cadastrarProduto(): void {

    if (!this.nome.trim() || this.preco === null || this.preco <= 0 || !this.descricao.trim()) {
      alert('Preencha todos os campos corretamente!');
      return;
    }

   this.produtos.push({
  nome: this.nome,
  preco: this.preco,
  descricao: this.descricao
});

if (isPlatformBrowser(this.platformId)) {
  localStorage.setItem('produtos', JSON.stringify(this.produtos));
}

console.log('Produtos armazenados:', localStorage.getItem('produtos'));
    alert('Produto cadastrado com sucesso!');

    this.nome = '';
    this.preco = null;
    this.descricao = '';
  }
  excluirProduto(index: number): void {

  const confirmar = confirm('Deseja realmente excluir este produto?');

  if (!confirmar) {
    return;
  }

  this.produtos.splice(index, 1);

  if (isPlatformBrowser(this.platformId)) {
    localStorage.setItem('produtos', JSON.stringify(this.produtos));
  }

  alert('Produto excluído com sucesso!');
}
}
