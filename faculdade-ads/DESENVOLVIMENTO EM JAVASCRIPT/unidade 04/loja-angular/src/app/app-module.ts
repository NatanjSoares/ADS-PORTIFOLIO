import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';

import { Cabecalho } from './components/cabecalho/cabecalho';
import { CadastroProduto } from './components/cadastro-produto/cadastro-produto';
import { ListaProdutos } from './components/lista-produtos/lista-produtos';

import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@NgModule({
  declarations: [
    App,
    Cabecalho,
    CadastroProduto,
    ListaProdutos
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    CommonModule
  ],
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideClientHydration()
  ],
  bootstrap: [App],
})
export class AppModule {}