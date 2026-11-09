import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CadastroProduto } from './components/cadastro-produto/cadastro-produto';
import { ListaProdutos } from './components/lista-produtos/lista-produtos';

const routes: Routes = [
  {
    path: '',
    component: CadastroProduto
  },
  {
    path: 'produtos',
    component: ListaProdutos
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}