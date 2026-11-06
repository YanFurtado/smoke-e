document.documentElement.classList.add("js");
const IMG={seda:"{{img:seda}}",zippo:"{{img:zippo}}",coroa:"{{img:coroa}}",grafite:"{{img:grafite}}",etiqueta:"{{img:etiqueta}}",trevo:"{{img:trevo}}",fumaca:"{{img:fumaca}}",smiley:"{{img:smiley}}",asterisco:"{{img:asterisco}}",logo:"{{img:logo-branco}}"};
/* Dados conferidos no Google Maps em 06/11/2026 */
const STORES={
  pnz:{code:"PNZ",city:"Petrolina",name:"Petrolina · PE",addr:"R. Joaquim Nabuco, 78 · Centro · Petrolina-PE · 56302-140",short:"R. Joaquim Nabuco, 78",score:"4,6",count:88,rating:"4,6 ★ no Google · 88 avaliações",phone:"5587988257595",phoneLabel:"(87) 98825-7595",cnpj:null,
    maps:"https://www.google.com/maps/search/?api=1&query=Tabacaria%20Smoke%20House&query_place_id=ChIJywkeWURwcwcRpd-Y7FuCcsg",eta:"20 a 60 min",hrs:{wk:[8,23],sun:[10,22]},
    bairros:[["Centro",5],["Areia Branca",7],["Vila Eduardo",6],["Cidade Universitária",8],["Jardim Maravilha",8],["José e Maria",8],["Gercino Coelho",9],["Dom Avelar",9],["João de Deus",9]]},
  lem:{code:"LEM",city:"LEM",name:"Luís Eduardo Magalhães · BA",addr:"Av. Juscelino Kubitschek, 2063 · Lot. Mimoso D'Oeste I · Luís Eduardo Magalhães-BA · 47850-013 · ao lado da Clínica Minotto",short:"Av. Juscelino Kubitschek, 2063",score:"5,0",count:58,rating:"5,0 ★ no Google · 58 avaliações",phone:"5577999879210",phoneLabel:"(77) 99987-9210",cnpj:null,
    maps:"https://www.google.com/maps/search/?api=1&query=Tabacaria%20Smoke%20House%20Lem&query_place_id=ChIJvbZQ37l3SpMRnX-nYZvazKI",eta:"no mesmo dia",hrs:{wk:[8,24],sun:[10,22]},bairros:[]}
};
const hh=h=>h>=24?"00h":String(h).padStart(2,"0")+"h";
const hoursTxt=st=>`Seg a Sáb · ${hh(st.hrs.wk[0])} às ${hh(st.hrs.wk[1])}<br>Dom · ${hh(st.hrs.sun[0])} às ${hh(st.hrs.sun[1])}`;
/* Avaliações públicas do Google Maps (trechos), sem nomes de autores */
const REVIEWS={
  lem:["Pedi delivery, foram super atenciosos no WhatsApp, chegou rápido e direitinho.","Impecável é a palavra! Diversas opções, é de ficar maravilhada. Atendimento muito top! Minha tabacaria favorita.","A melhor da região, produtos de ótima qualidade com preço acessível, e o atendimento perfeito com direito a um cafezinho maravilhoso."],
  pnz:["Melhor da região!! Produtos de qualidade e com grande variedade, ambiente climatizado e o melhor horário de funcionamento da cidade.","Ótimo atendimento, variedade enorme de produtos, ambiente excelente, climatizado e organizado. Embora haja outras na região, sempre dou prioridade a Smoke House.","Um local perfeito, ambiente com boa qualidade e produtos perfeitos."]
};
const SELLERS={carla:"Carla",joao:"João",bia:"Bia"};
const PAL={ZOMO:["#1b1d1a","#34925e"],ALEDA:["#7d1022","#c8243b"],PAPELITO:["#4a3216","#a8742d"],"BEM BOLADO":["#174a2e","#34925e"],OCB:["#1b1d1a","#55584f"],SMOKING:["#13305c","#3d6cc2"],LION:["#5a1840","#b6407f"],RAW:["#5d4220","#c7964b"],"PURE HEMP":["#2e4a17","#76a23a"],CLIPPER:["#1b1d1a","#e5383b"],ZIPPO:["#2a2b28","#8d8f87"],SQUADAFUM:["#0f3a40","#2aa3b5"],TATTOO:["#0e0f0d","#34925e"],VINHO:["#3d0f1d","#8a2340"],GIFT:["#5c4a18","#ffbe00"],INCENSO:["#5a2f12","#d07a2b"],GENERIC:["#1b1d1a","#3d403b"]};
const BNAME={ZOMO:"Zomo",ALEDA:"Aleda",PAPELITO:"Papelito","BEM BOLADO":"Bem Bolado",OCB:"OCB",SMOKING:"Smoking",LION:"Lion Rolling Circus",RAW:"Raw","PURE HEMP":"Pure Hemp",CLIPPER:"Clipper",ZIPPO:"Zippo",SQUADAFUM:"Squadafum",TATTOO:"Linha Tattoo",VINHO:"Vinhos selecionados",GIFT:"Smoke House",INCENSO:"Incensos",GENERIC:"Outras marcas"};
const P=[
 {id:1,cat:"Sedas",b:"ZOMO",n:"Seda Zomo King Size Brown",p:5,hot:1,sz:"King Size",pp:"Brown"},
 {id:2,cat:"Sedas",b:"ZOMO",n:"Seda Zomo King Size Rosa",p:5,sz:"King Size",pp:"Rosa"},
 {id:3,cat:"Sedas",b:"ALEDA",n:"Seda Aleda KS Clássica Vermelha",p:6,sz:"King Size",pp:"Branca"},
 {id:4,cat:"Sedas",b:"PAPELITO",n:"Seda Papelito King Size Brown Large",p:7,hot:1,sz:"King Size",pp:"Brown"},
 {id:5,cat:"Sedas",b:"PAPELITO",n:"Papelito Marrom c/ Piteira + Bandeja",p:15,hl:1,sz:"King Size",pp:"Brown"},
 {id:6,cat:"Sedas",b:"BEM BOLADO",n:"Seda Bem Bolado KS Large Hemp",p:8,sz:"King Size",pp:"Hemp"},
 {id:7,cat:"Sedas",b:"OCB",n:"OCB King Size Slim Premium",p:8,hl:1,sz:"KS Slim",pp:"Branca"},
 {id:8,cat:"Sedas",b:"OCB",n:"OCB King Size Slim Ultimate",p:10,sz:"KS Slim",pp:"Branca"},
 {id:9,cat:"Sedas",b:"SMOKING",n:"Seda Smoking King Size Deluxe",p:8,sz:"King Size",pp:"Branca"},
 {id:10,cat:"Sedas",b:"LION",n:"Lion Rolling Circus KS Alfafa",p:9,hot:1,sz:"King Size",pp:"Alfafa"},
 {id:11,cat:"Sedas",b:"RAW",n:"Seda Raw King Size Classic",p:10,hl:1,sz:"KS Slim",pp:"Brown"},
 {id:12,cat:"Sedas",b:"RAW",n:"Seda Raw KS Slim Organic Hemp",p:12,sz:"KS Slim",pp:"Hemp"},
 {id:13,cat:"Sedas",b:"PURE HEMP",n:"Seda Pure Hemp King Size",p:9,sz:"King Size",pp:"Hemp"},
 {id:20,cat:"Atacado",b:"ZOMO",n:"Caixa c/50 Seda Zomo KS Brown",p:120,hl:1,sz:"King Size",pp:"Brown"},
 {id:21,cat:"Atacado",b:"ZOMO",n:"Caixa c/50 Seda Zomo KS Branca",p:100,sz:"King Size",pp:"Branca"},
 {id:22,cat:"Atacado",b:"ZOMO",n:"Caixa c/25 Seda Zomo Monster KS",p:50,sz:"Monster",pp:"Brown"},
 {id:23,cat:"Atacado",b:"ZOMO",n:"Caixa c/25 Seda Zomo Mini Brown",p:40,sz:"Mini",pp:"Brown"},
 {id:30,cat:"Piteiras",b:"SQUADAFUM",n:"Piteira de vidro 6 mm",p:25,old:32,hot:1},
 {id:31,cat:"Piteiras",b:"BEM BOLADO",n:"Piteira de papel Large · bloco c/50",p:6},
 {id:40,cat:"Isqueiros",b:"CLIPPER",n:"Isqueiro Clipper Grande",p:18,hl:1,st:"zippo"},
 {id:41,cat:"Isqueiros",b:"ZIPPO",n:"Isqueiro Zippo Clássico",p:289,st:"zippo"},
 {id:42,cat:"Isqueiros",b:"SMOKING",n:"Isqueiro maçarico Smoking",p:45,old:59,hot:1,st:"zippo"},
 {id:50,cat:"Acessórios",b:"SQUADAFUM",n:"Dichavador de metal 4 partes 55 mm",p:79,hl:1},
 {id:51,cat:"Acessórios",b:"RAW",n:"Bandeja Raw média",p:69},
 {id:52,cat:"Acessórios",b:"GENERIC",n:"Bolador King Size 110 mm",p:15},
 {id:53,cat:"Acessórios",b:"GENERIC",n:"Pote hermético de vidro 120 ml",p:29},
 {id:60,cat:"Tattoo Supply",b:"TATTOO",n:"Cartucho tattoo RL · caixa c/20",p:89,old:110,hot:1,st:"coroa"},
 {id:61,cat:"Tattoo Supply",b:"TATTOO",n:"Pele artificial para treino",p:29,st:"coroa"},
 {id:62,cat:"Tattoo Supply",b:"TATTOO",n:"Filme protetor pós-tattoo 15 cm × 2 m",p:49,st:"coroa"},
 {id:63,cat:"Tattoo Supply",b:"TATTOO",n:"Pomada cicatrizante 50 g",p:35,st:"coroa"},
 {id:70,cat:"Vinhos",b:"VINHO",n:"Vinho tinto seco 750 ml",p:59,hl:1},
 {id:71,cat:"Vinhos",b:"VINHO",n:"Vinho branco suave 750 ml",p:49},
 {id:80,cat:"Presentes",b:"GIFT",n:"Kit presente Smoke House",p:99,hot:1,old:120,st:"etiqueta"},
 {id:81,cat:"Presentes",b:"INCENSO",n:"Incenso Massala sortido · 15 varetas",p:12,st:"fumaca"}
];
const OUT={pnz:[41,70,71],lem:[3,12,22,41,60,61]};
/* estoque por loja: compartilhado com a Área do vendedor */
const MIN_STOCK=5;
function getStock(store){let s=null;try{s=JSON.parse(localStorage.getItem("sh_stock_"+store))}catch(e){}
  if(!s){s={};P.forEach(p=>s[p.id]=OUT[store].includes(p.id)?0:(store==="pnz"?((p.id*7)%17)+2:((p.id*5)%13)+2));try{localStorage.setItem("sh_stock_"+store,JSON.stringify(s))}catch(e){}}return s}
function setStock(store,s){try{localStorage.setItem("sh_stock_"+store,JSON.stringify(s))}catch(e){}}
const CATS=["Sedas","Piteiras","Isqueiros","Acessórios","Tattoo Supply","Vinhos","Presentes","Atacado"];
const CIRCLES=[["Sedas","seda"],["Isqueiros","zippo"],["Tattoo Supply","coroa"],["Acessórios","grafite"],["Presentes","trevo"],["Atacado","etiqueta"]];
const POPULAR=["Raw","OCB","Zomo","Isqueiro","Tattoo Supply","Piteira de vidro","Caixa de seda","Kit presente"];
const PRICES=[["Até R$ 10",0,10],["R$ 10 a R$ 30",10,30],["R$ 30 a R$ 100",30,100],["Acima de R$ 100",100,1e9]];

/* =========================================================
   GUIAS (conteúdo educativo) e PÁGINAS DE CONFIANÇA
   ========================================================= */
const GUIDES=[
 {id:"seda",kicker:"Guia de compra",title:"Como escolher a sua seda",desc:"Tamanho, tipo de papel e espessura explicados em 3 minutos.",img:"seda",bg:"var(--yellow)",read:"3 min",prods:p=>p.cat==="Sedas",
  html:`<p class="lead">Seda parece tudo igual na prateleira, mas três escolhas mudam a experiência: o tamanho, o tipo de papel e a espessura. Este guia resume cada uma para você acertar na primeira compra.</p>
  <h2>1. Tamanho</h2><p>O tamanho define o comprimento da folha. A escolha depende de quanto você costuma usar por vez.</p>
  <div class="tbl"><table><thead><tr><th>Tamanho</th><th>Comprimento aproximado</th><th>Para quem</th></tr></thead><tbody>
  <tr><td>Mini</td><td>70 mm</td><td>Quem usa pouca quantidade</td></tr>
  <tr><td>1¼</td><td>78 mm</td><td>Meio-termo, o mais versátil</td></tr>
  <tr><td>King Size</td><td>108 a 110 mm</td><td>Quem prefere folha longa</td></tr>
  <tr><td>King Size Slim</td><td>108 mm, mais estreita</td><td>Folha longa com menos papel</td></tr>
  <tr><td>Monster</td><td>maior que KS</td><td>Uso compartilhado</td></tr></tbody></table></div>
  <h2>2. Tipo de papel</h2>
  <ul><li><b>Branca:</b> o papel tradicional, com acabamento uniforme.</li>
  <li><b>Brown:</b> papel não branqueado, de cor natural. Muita gente prefere por ter menos processamento.</li>
  <li><b>Hemp (cânhamo):</b> fibra natural, com textura um pouco mais firme na hora de enrolar.</li>
  <li><b>Alfafa e orgânicas:</b> fibras vegetais alternativas, com acabamento diferente ao toque.</li></ul>
  <h2>3. Espessura</h2><p>Quanto mais fina a folha, menos papel você usa. As versões <b>slim</b> e <b>ultra fina</b> pedem um pouco mais de prática para enrolar, enquanto a espessura normal é mais fácil para quem está começando.</p>
  <div class="callout">Ainda em dúvida? Leve um livreto de cada tipo e compare. Na promoção da semana, <b>levando 3 sedas, você paga 2</b>.</div>
  <h2>Livreto ou caixa?</h2><p>Se você usa sempre o mesmo modelo, a caixa fechada sai mais em conta por livreto. É a mesma opção que tabacarias e conveniências usam para revenda, na categoria Atacado.</p>`},
 {id:"tattoo",kicker:"Tattoo Supply",title:"Começando na tatuagem: para que serve cada material",desc:"Cartucho, tinta, pele de treino e pós-tattoo sem confusão.",img:"coroa",bg:"var(--green)",read:"4 min",prods:p=>p.cat==="Tattoo Supply",
  html:`<p class="lead">Quem está começando costuma comprar material demais ou o material errado. Este guia separa o que cada item faz, para você montar a primeira lista com segurança.</p>
  <h2>Cartuchos</h2><p>São as agulhas descartáveis e estéreis que vão na máquina. A sigla na caixa indica a configuração: <b>RL</b> (round liner) é usada para contorno e traço; <b>RS</b> e <b>M1</b> (magnum) servem para preenchimento e sombreamento. O número indica quantas agulhas o cartucho tem.</p>
  <h2>Tintas</h2><p>Existe tinta pensada para <b>contorno</b> e tinta pensada para <b>preenchimento</b>, além de diferentes cores e consistências.</p>
  <div class="callout warn"><b>Antes de comprar tinta para outra pessoa,</b> pergunte ao tatuador qual tipo e qual marca ele usa. Nossa equipe confirma pelo WhatsApp se temos exatamente o que foi pedido.</div>
  <h2>Pele artificial</h2><p>Placa de silicone para treinar traço, sombra e profundidade antes de atender pessoas. É o melhor investimento de quem ainda está aprendendo.</p>
  <h2>Barreira e descartáveis</h2><p>Luvas, filme plástico para cobrir a máquina e os equipamentos, batoques e papel toalha fazem parte da rotina de biossegurança de qualquer estúdio.</p>
  <h2>Pós-tattoo</h2><p>O <b>filme protetor</b> cobre a tatuagem nas primeiras horas, e a <b>pomada cicatrizante</b> ajuda no cuidado dos dias seguintes, conforme a orientação do tatuador.</p>
  <h2>Checklist da primeira compra</h2><ol><li>Cartuchos RL para traço e RS ou M1 para preenchimento</li><li>Tinta preta de contorno</li><li>Pele artificial para treino</li><li>Luvas, filme de barreira e batoques</li><li>Filme protetor e pomada pós-tattoo</li></ol>
  <p style="font-size:13px;color:var(--muted)">Material de tatuagem não substitui formação. Procure curso e orientação de biossegurança antes de atender.</p>`},
 {id:"presente",kicker:"Ideias de presente",title:"Três tipos de pessoa, três ideias de presente",desc:"Do colecionador ao prático: acerte o presente sem complicar.",img:"trevo",bg:"var(--ink)",read:"2 min",prods:p=>p.cat==="Presentes"||p.cat==="Isqueiros"||p.cat==="Vinhos",
  html:`<p class="lead">Escolher presente fica mais fácil quando você começa pela pessoa, não pelo produto. Separamos três perfis que aparecem todo dia no balcão.</p>
  <h2>1. O colecionador</h2><p>Gosta de objeto bonito e durável. Um <b>Zippo clássico</b> é presente para a vida toda e ainda pode ser personalizado.</p>
  <h2>2. Quem recebe os amigos</h2><p>Para quem gosta de reunir a turma em casa, um <b>vinho</b> da seleção da loja de LEM é aposta segura. Conte para a equipe a ocasião e o valor, e a gente indica.</p>
  <h2>3. O prático</h2><p>Prefere coisa útil. O <b>kit presente Smoke House</b> já vem montado, com embalagem pronta para entregar.</p>
  <div class="callout">Não sabe o que a pessoa usa? Fale com a loja pelo WhatsApp: a equipe monta um kit dentro do seu orçamento.</div>
  <p style="font-size:13px;color:var(--muted)">Venda de bebidas alcoólicas e produtos de tabacaria proibida para menores de 18 anos.</p>`}
];
const PAGES={
 guias:{title:"Guias Smoke House",kicker:"Conteúdo",html:()=>`<p class="lead">Explicações rápidas para você comprar certo, escritas por quem atende no balcão todos os dias.</p><div class="guides" style="margin-top:10px">${GUIDES.map(guideCard).join("")}</div>`},
 sobre:{title:"Quem somos",kicker:"Institucional",html:()=>`<p class="lead">A Smoke House é uma tabacaria e head shop com duas lojas: no Centro de Petrolina (PE), há 13 anos, e em Luís Eduardo Magalhães (BA).</p>
  <p>Reunimos as linhas tradicionais de tabacaria, acessórios, presentes e a linha <b>Tattoo Supply</b> para tatuadores e estúdios. Na loja de LEM, você também encontra uma seleção de vinhos.</p>
  <p>Nosso jeito de atender é simples: você conta o que procura e um colaborador ajuda a escolher. Pelo site ou pelo WhatsApp, você consulta, reserva e retira na loja, ou recebe em casa.</p>
  <h2>Nossas lojas</h2>${Object.values(STORES).map(st=>`<p><b>${st.name}</b><br>${esc(st.addr)}<br>${hoursTxt(st).replace("<br>"," · ")}<br>WhatsApp ${st.phoneLabel} · ${st.rating}</p>`).join("")}`},
 entrega:{title:"Entrega e retirada",kicker:"Ajuda",html:()=>`<p class="lead">Você escolhe no checkout se prefere retirar na loja ou receber em casa.</p>
  <h2>Retirada na loja</h2><p>Gratuita. Escolha o horário no checkout e apresente o número do pedido e um documento com foto. Pedidos marcados como "o quanto antes" ficam prontos em até 20 minutos.</p>
  <h2>Entrega em Petrolina</h2><p>Prazo de 20 a 60 minutos dentro do horário da loja, com taxa calculada por bairro no checkout.</p>
  <h2>Entrega em Luís Eduardo Magalhães</h2><p>Entrega no mesmo dia, com taxa confirmada pela loja no WhatsApp.</p>
  <div class="callout warn"><b>Maioridade:</b> o entregador ou o colaborador confere um documento com foto. Sem documento de pessoa maior de 18 anos, o pedido não é entregue.</div>
  <p>Todos os pedidos saem em embalagem discreta, sem identificação do conteúdo.</p>`},
 trocas:{title:"Trocas e devoluções",kicker:"Ajuda",html:()=>`<p class="lead">Queremos que você saia satisfeito. Estas são as regras para trocar ou devolver um produto.</p>
  <h2>Arrependimento em compras pelo site</h2><p>Compras feitas pelo site ou pelo WhatsApp podem ser canceladas em até <b>7 dias corridos</b> após o recebimento, como garante o Código de Defesa do Consumidor. O valor pago é devolvido integralmente.</p>
  <h2>Produto com defeito</h2><p>Avise a loja pelo WhatsApp com foto do problema. O prazo para reclamar é de 30 dias para produtos não duráveis e de 90 dias para produtos duráveis, contados do recebimento. Fazemos a troca, o conserto ou a devolução do valor.</p>
  <h2>Comprou o item errado?</h2><p>Se o produto estiver lacrado e sem uso, trocamos por outro da loja. Para materiais de tatuagem, consulte a equipe antes da compra: confirmamos a referência certa com você ou com o seu tatuador.</p>
  <h2>Itens estéreis e de higiene</h2><p>Por segurança sanitária, cartuchos, agulhas e itens de uso pessoal só voltam ao estoque com a embalagem original lacrada.</p>
  <h2>Como solicitar</h2><p>Fale com a loja onde você comprou, informe o número do pedido e o motivo. Respondemos no mesmo dia, dentro do horário de funcionamento.</p>`},
 privacidade:{title:"Privacidade e cookies",kicker:"LGPD",html:()=>`<p class="lead">Explicamos aqui quais dados coletamos, para quê e como você controla essas informações, conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018).</p>
  <h2>Dados que coletamos</h2><ul><li><b>No pedido:</b> nome, WhatsApp, data de nascimento e, se você escolher entrega, o endereço.</li><li><b>Na navegação:</b> páginas visitadas e produtos adicionados ao carrinho, somente se você aceitar os cookies de medição.</li></ul>
  <h2>Para que usamos</h2><ul><li>Processar, entregar e dar suporte ao seu pedido.</li><li>Confirmar a maioridade, exigência legal para a venda destes produtos.</li><li>Com a sua permissão, medir o uso do site e mostrar ofertas mais relevantes.</li></ul>
  <h2>Com quem compartilhamos</h2><p>Apenas com quem participa do pedido, como o entregador e o meio de pagamento, e com ferramentas de medição quando você autoriza. Não vendemos seus dados.</p>
  <h2>Cookies</h2><p><b>Essenciais:</b> guardam o carrinho, a loja escolhida e a confirmação de idade. <b>Medição:</b> ferramentas de análise e de anúncios, que só são ativadas se você aceitar. Você pode mudar a escolha a qualquer momento abaixo.</p>
  <p><button class="btn btn-dark" data-cookie-reset="1">Rever minha escolha de cookies</button></p>
  <h2>Seus direitos</h2><p>Você pode pedir acesso, correção, portabilidade ou exclusão dos seus dados, e retirar o consentimento, pelo WhatsApp da loja.</p>`},
 termos:{title:"Termos de uso",kicker:"Institucional",html:()=>`<h2>Maioridade</h2><p>O site e as compras são exclusivos para maiores de 18 anos. A idade é informada no acesso, validada no checkout e conferida com documento na entrega ou retirada.</p>
  <h2>Preços e estoque</h2><p>Preços e estoque variam entre as lojas de Petrolina e de Luís Eduardo Magalhães. O pedido só é confirmado depois do contato da loja pelo WhatsApp.</p>
  <h2>Imagens</h2><p>As imagens são ilustrativas. Cores e estampas podem variar conforme o lote do fabricante.</p>
  <h2>Uso responsável</h2><p>Não vendemos cigarros eletrônicos. Produtos de tabacaria fazem mal à saúde.</p>`},
 promocoes:{title:"Regras de promoção",kicker:"Ajuda",html:()=>`<h2>Leve 3, pague 2 em sedas</h2><p>Válido para as sedas marcadas com a etiqueta "3 por 2". A cada 3 unidades no carrinho, a de menor valor sai de graça. O desconto aparece automaticamente.</p>
  <h2>5% no Pix</h2><p>Pagando no Pix, você ganha 5% de desconto sobre os produtos. O desconto vale junto com o 3 por 2 e não se aplica à taxa de entrega.</p>
  <h2>#PRIMEIRACOMPRA</h2><p>5% de desconto na primeira compra pelo site, um uso por CPF. Não cumulativo com o desconto do Pix.</p>
  <p style="font-size:13px;color:var(--muted)">Promoções válidas enquanto durar o estoque de cada loja.</p>`},
 pagamento:{title:"Formas de pagamento",kicker:"Ajuda",html:()=>`<p class="lead">Aceitamos as principais formas de pagamento do mercado, no site, na entrega e no balcão das duas lojas.</p>${PAYMENTS.map(p=>`<h2>${p.l}</h2><p>${p.info}</p>`).join("")}<div class="pay" style="margin-top:18px">${PAY_BRANDS.map(b=>`<span>${b}</span>`).join("")}</div><div class="callout">O desconto de 5% vale só para o Pix e é aplicado automaticamente no checkout.</div>`}
};
function guideCard(g){return `<button class="guide rv" data-guide="${g.id}"><div class="gi" style="background:${g.bg}"><img src="${IMG[g.img]}" alt=""></div><div class="gb"><span>${g.kicker} · ${g.read}</span><b>${g.title}</b><small>${g.desc}</small></div></button>`}

/* =========================================================
   FORMAS DE PAGAMENTO (cadastro único usado em todo o sistema)
   ========================================================= */
const PAYMENTS=[
  {k:"pix",l:"Pix",short:"Pix",c:"#34925e",desc:"5% de desconto · QR code ou chave enviados no WhatsApp",info:"Aprovação na hora. Enviamos o QR code ou a chave Pix pelo WhatsApp da loja assim que o pedido é confirmado."},
  {k:"credito",l:"Cartão de crédito",short:"Crédito",c:"#0e0f0d",desc:"Até 3x sem juros · Visa, Mastercard, Elo, Hipercard, Amex",info:"Até 3x sem juros a partir de R$ 60 (parcela mínima de R$ 30). Pague pelo link seguro enviado no WhatsApp ou na maquininha, na entrega ou na retirada. Aceitamos Visa, Mastercard, Elo, Hipercard, American Express e Diners."},
  {k:"debito",l:"Cartão de débito",short:"Débito",c:"#3d6cc2",desc:"Na maquininha, na entrega ou na retirada",info:"Na maquininha, na entrega ou na retirada. Aceitamos Visa Débito, Maestro e Elo Débito."},
  {k:"carteira",l:"Carteira digital",short:"Carteira",c:"#7a52c7",desc:"Apple Pay, Google Pay, Samsung Pay, PicPay ou Mercado Pago",info:"Apple Pay, Google Pay e Samsung Pay por aproximação na maquininha. PicPay e Mercado Pago pelo QR code enviado no WhatsApp."},
  {k:"boleto",l:"Boleto bancário",short:"Boleto",c:"#a87700",desc:"Para atacado e revenda · separado após a compensação",info:"Indicado para compras de atacado e revenda. O boleto é enviado pelo WhatsApp e o pedido é separado após a compensação, em até 2 dias úteis."},
  {k:"dinheiro",l:"Dinheiro",short:"Dinheiro",c:"#ffbe00",desc:"Na entrega ou na retirada · informe o troco",info:"Na entrega ou na retirada. Informe no checkout se precisa de troco."}
];
const PAYK=k=>k==="cartao"?"credito":k;           /* pedidos antigos usavam "cartao" */
const payOf=k=>PAYMENTS.find(p=>p.k===PAYK(k))||PAYMENTS[1];
const payLabel=(o,long)=>{const p=payOf(o.pag);let s=long?p.l:p.short;if(p.k==="credito"&&o.parc>1)s+=` em ${o.parc}x sem juros`;if(p.k==="dinheiro"&&o.troco)s+=` · troco para R$ ${o.troco}`;return s};
const maxParc=v=>v>=60?Math.min(3,Math.floor(v/30)):1;
const PAY_BRANDS=["PIX","VISA","MASTERCARD","ELO","HIPERCARD","AMEX","DINERS","BOLETO","APPLE PAY","GOOGLE PAY","PICPAY","MERCADO PAGO"];

const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const brl=v=>v.toLocaleString("pt-BR",{style:"currency",currency:"BRL"});
const ls={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
const lsj={get(k,d){try{return JSON.parse(ls.get(k))??d}catch(e){return d}},set(k,v){ls.set(k,JSON.stringify(v))}};
const RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
const newF=()=>({brands:new Set(),sz:new Set(),pp:new Set(),price:null,avail:false,promo:false});
let S={store:null,seller:null,view:"home",cat:null,q:"",sort:"rel",cart:{},f:newF(),co:null,lastOrder:null};

const grad=b=>{const c=PAL[b]||PAL.GENERIC;return `linear-gradient(140deg,${c[0]},${c[1]})`};
const tl=p=>p.b==="TATTOO"?"Tattoo":p.b==="GIFT"?"Kit":p.b==="VINHO"?"Vinho":p.b.toLowerCase();
const isOut=p=>(getStock(S.store)[p.id]??0)<=0;
function show(id){["v-age","v-city","v-store","v-seller","v-owner"].forEach(v=>$("#"+v).hidden=v!==id);if(id!=="v-store"){$("#bnav").hidden=true;$("#wa-fab").hidden=true;$("#cookie").hidden=true;document.body.classList.remove("has-bnav")}window.scrollTo(0,0);Smoke.refresh()}
function toast(t){const el=$("#toast");el.textContent=t;el.classList.add("on");clearTimeout(toast.t);toast.t=setTimeout(()=>el.classList.remove("on"),2200)}
function openNow(st){const d=new Date(),h=d.getHours()+d.getMinutes()/60,r=d.getDay()===0?st.hrs.sun:st.hrs.wk;return h>=r[0]&&h<r[1]}

function parseHash(){const m=location.hash.slice(1).match(/^(lem|pnz)(?:-vendedor-([a-z]+))?$/);return m?{store:m[1],seller:SELLERS[m[2]]||null}:null}
function route(){
  if(location.hash==="#colaborador"){show("v-seller");renderSV();return}
  if(location.hash==="#donos"){show("v-owner");renderOW();return}
  if(ls.get("sh_age")!=="ok"){show("v-age");return}
  const r=parseHash();
  if(!r){show("v-city");return}
  if(S.store!==r.store){S.cart={};S.view="home";S.q="";$("#q").value=""}
  S.store=r.store;S.seller=r.seller;renderAll();show("v-store");
}

/* =========================================================
   BUSCA: normalização, sinônimos e tolerância a erro
   ========================================================= */
const norm=s=>String(s).normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase().replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ").trim();
const SYN={isqueiro:["acendedor","macarico","zippo","clipper","isqueiros"],seda:["papel","sedas","papelito","livreto"],tattoo:["tatuagem","tatuador","tatoo","tatto","cartucho","pele"],presente:["kit","presentes","gift"],piteira:["filtro","tip","piteiras"],vinho:["vinhos","tinto","branco"],atacado:["caixa","revenda","caixas"],dichavador:["triturador","moedor"],bandeja:["bandejas"],incenso:["incensos"]};
const SYNMAP={};Object.entries(SYN).forEach(([k,v])=>{SYNMAP[k]=k;v.forEach(x=>SYNMAP[x]=k)});
P.forEach(p=>{
  const base=norm([p.n,p.b,BNAME[p.b],p.cat,p.sz||"",p.pp||""].join(" "));
  const extra=new Set();base.split(" ").forEach(w=>{const k=SYNMAP[w];if(k){extra.add(k);SYN[k].forEach(x=>extra.add(x))}});
  p._h=base+" "+[...extra].join(" ");p._w=[...new Set(p._h.split(" "))];
});
const VOCAB=[...new Set(P.flatMap(p=>norm([p.n,BNAME[p.b],p.cat].join(" ")).split(" ")).concat(Object.keys(SYN)).filter(w=>w.length>=3))];
function lev(a,b){if(Math.abs(a.length-b.length)>2)return 9;const m=a.length,n=b.length;let prev=Array.from({length:n+1},(_,j)=>j);for(let i=1;i<=m;i++){const cur=[i];for(let j=1;j<=n;j++)cur[j]=Math.min(prev[j]+1,cur[j-1]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1));prev=cur}return prev[n]}
const tol=w=>w.length>=7?2:w.length>=4?1:0;
function search(q){
  const toks=norm(q).split(" ").filter(Boolean);if(!toks.length)return{res:[],fixed:null};
  let fixedWords=[],usedFix=false;
  const res=P.map(p=>{
    let score=0;
    for(const t of toks){
      if(p._h.includes(t)){score+=p._w.some(w=>w.startsWith(t))?4:2;continue}
      const syn=SYNMAP[t];if(syn&&p._h.includes(syn)){score+=3;continue}
      const k=tol(t);if(!k)return null;
      let best=null;for(const w of p._w){if(w.length<3)continue;const d=lev(t,w.slice(0,Math.max(t.length,Math.min(w.length,t.length+1))));if(d<=k&&(!best||d<best.d))best={w,d}}
      if(!best)return null;score+=1.5-best.d*.4;usedFix=true;
    }
    if(p.hl)score+=.3;if(isOut(p))score-=.5;return{p,score};
  }).filter(Boolean).sort((a,b)=>b.score-a.score).map(x=>x.p);
  if(usedFix){fixedWords=toks.map(t=>{if(VOCAB.includes(t)||VOCAB.some(w=>w.startsWith(t)))return t;let best=t,bd=9;for(const w of VOCAB){const d=lev(t,w);if(d<bd&&d<=tol(t)){bd=d;best=w}}return best})}
  const fixed=usedFix&&fixedWords.join(" ")!==toks.join(" ")?fixedWords.join(" "):null;
  return{res,fixed};
}
function hl(text,q){
  const toks=norm(q).split(" ").filter(t=>t.length>1);if(!toks.length)return esc(text);
  const n=norm(text).split("");// mapa simples por posição
  const raw=String(text),plain=raw.normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
  const marks=new Array(raw.length).fill(false);
  toks.forEach(t=>{let i=plain.indexOf(t);while(i>-1){for(let k=i;k<i+t.length;k++)marks[k]=true;i=plain.indexOf(t,i+1)}});
  let out="",open=false;for(let i=0;i<raw.length;i++){if(marks[i]&&!open){out+="<mark>";open=true}if(!marks[i]&&open){out+="</mark>";open=false}out+=esc(raw[i])}if(open)out+="</mark>";return out;
}

/* ---- autocomplete ---- */
const AC={el:null,idx:-1};
function recent(){return lsj.get("sh_recent",[])}
function pushRecent(q){const r=[q,...recent().filter(x=>norm(x)!==norm(q))].slice(0,5);lsj.set("sh_recent",r)}
function acOpen(o){const el=$("#ac");if(o)el.querySelectorAll("button").forEach(b=>b.type="button");else el.querySelectorAll(".act").forEach(x=>x.classList.remove("act"));el.hidden=!o;$("#q").setAttribute("aria-expanded",String(o));AC.idx=-1}
function renderAC(){
  const q=$("#q").value.trim(),el=$("#ac");
  if(!q){
    const r=recent();
    el.innerHTML=(r.length?`<div class="ac-sec">Buscas recentes</div><div class="ac-chips">${r.map(x=>`<button class="ac-nav" data-acq="${esc(x)}">${esc(x)}</button>`).join("")}</div>`:"")+
      `<div class="ac-sec">Mais procurados</div><div class="ac-chips">${POPULAR.map(x=>`<button class="ac-nav" data-acq="${esc(x)}">${esc(x)}</button>`).join("")}</div>`;
    acOpen(true);return;
  }
  const {res,fixed}=search(q);
  const nq=norm(q);const cats=CATS.filter(c=>norm(c).includes(nq)||nq.split(" ").some(t=>t.length>2&&(norm(c).startsWith(t)||SYNMAP[t]&&norm(c).includes(SYNMAP[t]))));
  if(!res.length){
    el.innerHTML=`<div class="ac-empty">Nenhum produto encontrado para <b>“${esc(q)}”</b>.</div><div class="ac-sec">Experimente</div><div class="ac-chips">${POPULAR.slice(0,6).map(x=>`<button class="ac-nav" data-acq="${esc(x)}">${esc(x)}</button>`).join("")}</div>`;
    acOpen(true);return;
  }
  el.innerHTML=(fixed?`<div class="ac-fix">Mostrando resultados para <button class="ac-nav" data-acq="${esc(fixed)}">${esc(fixed)}</button></div>`:"")+
    (cats.length?`<div class="ac-sec">Categorias</div><div class="ac-chips">${cats.map(c=>`<button class="ac-nav" data-go="${esc(c)}">${esc(c)}</button>`).join("")}</div>`:"")+
    `<div class="ac-sec">Produtos</div>`+
    res.slice(0,6).map(p=>`<button class="ac-item ac-nav" data-pid="${p.id}"><span class="mini" style="background:${grad(p.b)}">${tl(p)}</span><span><b>${hl(p.n,fixed||q)}</b><small>${esc(p.cat)} · ${esc(BNAME[p.b])}</small></span><span class="pr ${isOut(p)?"out":""}">${isOut(p)?"Esgotado":brl(p.p)}</span></button>`).join("")+
    `<button class="ac-foot ac-nav" data-acall="1">Ver todos os ${res.length} resultados para “${esc(q)}” →</button>`;
  acOpen(true);
}
function acMove(d){
  const items=[...document.querySelectorAll("#ac .ac-nav")];if(!items.length)return;
  items.forEach(i=>i.classList.remove("act"));AC.idx=(AC.idx+d+items.length)%items.length;
  const it=items[AC.idx];it.classList.add("act");it.scrollIntoView({block:"nearest"});
}
function doSearch(q){
  q=q.trim();if(!q)return;$("#q").value=q;pushRecent(q);acOpen(false);$("#q").blur();
  S.q=q;S.cat=null;S.view="list";S.f=newF();$("#mega").hidden=true;renderChrome();renderView();window.scrollTo(0,0);
}

/* =========================================================
   CARDS / HOME
   ========================================================= */
function card(p,delay){
  const out=isOut(p),pix=p.p*0.95,n=Math.min(3,Math.floor(p.p/30));
  const tag=out?'<span class="tag out">Esgotado nesta loja</span>':p.old?`<span class="tag">-${Math.round((1-p.p/p.old)*100)}%</span>`:(p.hot&&p.cat==="Sedas")?'<span class="tag">3 por 2</span>':"";
  const inst=p.p>=60?`ou <b>${n}x de ${brl(p.p/n)}</b> sem juros`:`ou <b>${brl(p.p)}</b> no cartão`;
  return `<article class="card"${delay!=null?` style="animation-delay:${delay}ms"`:""} data-card="${p.id}">
    <div class="thumb" style="background:${grad(p.b)}">${tag}<span class="brand">${tl(p)}</span>${p.st?`<img class="mark" src="${IMG[p.st]}" alt="">`:""}</div>
    <div class="card-body">
      <h4>${esc(p.n)}</h4>
      ${p.old?`<span class="old">${brl(p.old)}</span>`:'<span class="old" style="visibility:hidden">-</span>'}
      <span class="pix">${brl(pix)}<small>no Pix</small></span>
      <span class="inst">${inst}</span>
      <button class="add" data-add="${p.id}" ${out?"disabled":""}>${out?"Indisponível":"Adicionar ao carrinho"}</button>
    </div></article>`;
}
function shelfItems(k){return k==="hl"?P.filter(p=>p.hl):k==="hot"?P.filter(p=>p.hot):P.filter(p=>p.cat===k)}
function renderHome(){
  $("#circles").innerHTML=CIRCLES.map(([c,s],i)=>`<button class="circle rv-pop" style="transition-delay:${i*70}ms" data-go="${c}"><i><img src="${IMG[s]}" alt=""></i>${c}</button>`).join("");
  document.querySelectorAll("[data-shelf]").forEach(sec=>{
    sec.querySelector(".shelf-wrap")?.remove();
    const w=document.createElement("div");w.className="shelf-wrap rv";
    w.innerHTML=`<button class="s-arrow s-prev" aria-label="Anterior">‹</button><div class="shelf">${shelfItems(sec.dataset.shelf).map(p=>card(p)).join("")}</div><button class="s-arrow s-next" aria-label="Próximo">›</button>`;
    sec.appendChild(w);
  });
  $("#stores").innerHTML=Object.entries(STORES).map(([k,st])=>{
    const open=openNow(st);
    return `<article class="storecard rv ${k===S.store?"cur":""}">
      <div class="facade"><img src="${IMG.logo}" alt=""><span class="door"></span><small>Fachada ${st.code} · trocar pela foto do Google</small></div>
      <div class="sc-info">
        <h4>${st.name}<span>${st.code}</span></h4>
        <span class="open ${open?"":"closed"}"><i></i>${open?"Aberto agora":"Fechado agora"}</span>
        <dl class="kv"><dt>Endereço</dt><dd>${esc(st.addr)}</dd><dt>Horário</dt><dd>${hoursTxt(st)}</dd><dt>Google</dt><dd>${st.rating}</dd><dt>WhatsApp</dt><dd>${st.phoneLabel}</dd></dl>
        <div class="sc-actions"><a class="btn btn-dark" target="_blank" rel="noopener" href="${st.maps}">Ver no mapa</a>${k!==S.store?`<button class="btn btn-line" data-store-go="${k}">Comprar nesta loja</button>`:'<span class="note" style="align-self:center">Loja selecionada</span>'}</div>
      </div></article>`}).join("");
  /* avaliações: loja atual primeiro */
  const order=[S.store,...Object.keys(STORES).filter(k=>k!==S.store)];
  $("#rev-top").innerHTML=order.map(k=>{const st=STORES[k];return `<div class="rev-score"><span class="big">${st.score}</span><div><span class="stars-row">${"★".repeat(Math.round(parseFloat(st.score.replace(",","."))))}</span><b>Smoke House ${st.code}</b><small>${st.count} avaliações no Google</small></div><a href="${st.maps}" target="_blank" rel="noopener">Ver no Google →</a></div>`}).join("");
  $("#rev-track").innerHTML=order.flatMap(k=>REVIEWS[k].map(r=>`<article class="rev"><span class="stars-row">★★★★★</span><p>${esc(r)}</p><footer><span>Cliente no Google</span><b>Loja ${STORES[k].code}</b></footer></article>`)).join("");
  $("#guides").innerHTML=GUIDES.map(g=>guideCard(g)).join("");
  observe();
}

/* =========================================================
   LISTAGEM + FILTROS
   ========================================================= */
let lastFix=null;
function baseList(){
  lastFix=null;
  if(S.q){const r=search(S.q);lastFix=r.fixed;return r.res}
  if(S.cat==="promo")return P.filter(p=>p.hot);
  if(S.cat==="Destaques")return P.filter(p=>p.hl);
  return P.filter(p=>p.cat===S.cat);
}
function passes(p,f,skip){
  if(skip!=="brands"&&f.brands.size&&!f.brands.has(p.b))return false;
  if(skip!=="sz"&&f.sz.size&&!f.sz.has(p.sz))return false;
  if(skip!=="pp"&&f.pp.size&&!f.pp.has(p.pp))return false;
  if(skip!=="price"&&f.price!=null){const r=PRICES[f.price];if(p.p<r[1]||p.p>=r[2])return false}
  if(skip!=="avail"&&f.avail&&isOut(p))return false;
  if(skip!=="promo"&&f.promo&&!p.hot)return false;
  return true;
}
function fCount(f){return f.brands.size+f.sz.size+f.pp.size+(f.price!=null?1:0)+(f.avail?1:0)+(f.promo?1:0)}
function listItems(){
  let l=baseList().filter(p=>passes(p,S.f));
  if(S.sort==="asc")l=[...l].sort((a,b)=>a.p-b.p);
  if(S.sort==="desc")l=[...l].sort((a,b)=>b.p-a.p);
  if(S.sort==="off")l=[...l].sort((a,b)=>((b.old?1-b.p/b.old:b.hot?.33:0)-(a.old?1-a.p/a.old:a.hot?.33:0)));
  return l;
}
function facet(base,key,getter){
  const all=new Map();base.forEach(p=>{const v=getter(p);if(v)all.set(v,0)});
  base.filter(p=>passes(p,S.f,key)).forEach(p=>{const v=getter(p);if(v)all.set(v,all.get(v)+1)});
  return [...all.entries()];
}
function renderFilters(){
  const base=baseList(),f=S.f,st=STORES[S.store];
  const grp=(title,key,items,label)=>items.length>1||f[key].size?`<div class="f-group"><h5>${title}</h5>${items.sort((a,b)=>String(label?label(a[0]):a[0]).localeCompare(String(label?label(b[0]):b[0]))).map(([v,c])=>`<label class="f-opt ${!c&&!f[key].has(v)?"dis":""}"><input type="checkbox" data-f="${key}" value="${esc(v)}" ${f[key].has(v)?"checked":""} ${!c&&!f[key].has(v)?"disabled":""}><span>${esc(label?label(v):v)}</span><em>${c}</em></label>`).join("")}</div>`:"";
  const brands=facet(base,"brands",p=>p.b),sz=facet(base,"sz",p=>p.sz),pp=facet(base,"pp",p=>p.pp);
  const prices=PRICES.map((r,i)=>[i,base.filter(p=>passes(p,f,"price")&&p.p>=r[1]&&p.p<r[2]).length]);
  const nAvail=base.filter(p=>passes(p,f,"avail")&&!isOut(p)).length,nPromo=base.filter(p=>passes(p,f,"promo")&&p.hot).length;
  const n=fCount(f),total=listItems().length;
  $("#filters").innerHTML=`<div class="f-head"><b>Filtros</b>${n?`<button class="f-clear" data-fclear="1">Limpar tudo</button>`:""}</div>
    <div class="f-group">
      <label class="f-toggle"><span>Disponível na loja ${st.code} <em style="font-style:normal;color:var(--muted);font-size:11.5px">(${nAvail})</em></span><span class="sw"><input type="checkbox" data-fsw="avail" ${f.avail?"checked":""}><i></i></span></label>
      <label class="f-toggle"><span>Em promoção <em style="font-style:normal;color:var(--muted);font-size:11.5px">(${nPromo})</em></span><span class="sw"><input type="checkbox" data-fsw="promo" ${f.promo?"checked":""}><i></i></span></label>
    </div>
    ${grp("Marca","brands",brands,v=>BNAME[v])}
    <div class="f-group"><h5>Preço</h5>${prices.map(([i,c])=>`<label class="f-opt ${!c&&f.price!==i?"dis":""}"><input type="radio" name="fprice" data-fprice="${i}" ${f.price===i?"checked":""} ${!c&&f.price!==i?"disabled":""}><span>${PRICES[i][0]}</span><em>${c}</em></label>`).join("")}${f.price!=null?`<button class="f-clear" data-fprice-clear="1" style="margin-top:4px">Qualquer preço</button>`:""}</div>
    ${grp("Tamanho","sz",sz)}
    ${grp("Tipo de papel","pp",pp)}
    <button class="btn btn-green f-apply" data-fclose="1">Ver ${total} ${total===1?"produto":"produtos"}</button>`;
  $("#f-n").hidden=!n;$("#f-n").textContent=n;
  const chips=[];
  if(f.avail)chips.push(["avail",null,`Disponível na ${st.code}`]);
  if(f.promo)chips.push(["promo",null,"Em promoção"]);
  f.brands.forEach(v=>chips.push(["brands",v,BNAME[v]]));
  if(f.price!=null)chips.push(["price",null,PRICES[f.price][0]]);
  f.sz.forEach(v=>chips.push(["sz",v,v]));f.pp.forEach(v=>chips.push(["pp",v,"Papel "+v]));
  $("#chips-on").innerHTML=chips.map(([k,v,l])=>`<button data-chip="${k}" data-v="${esc(v??"")}" aria-label="Remover filtro ${esc(l)}">${esc(l)}</button>`).join("")+(chips.length>1?`<button class="clr" data-fclear="1">Limpar filtros</button>`:"");
}
function renderListing(){
  const base=baseList();
  const name=S.q?`Busca: “${S.q}”`:S.cat==="promo"?"Ofertas da semana":S.cat==="Destaques"?"Mais vendidos":S.cat;
  $("#list-title").textContent=name;$("#crumb-cur").textContent=name;
  const l=listItems();
  $("#list-count").innerHTML=(lastFix?`Mostrando resultados para <b>“${esc(lastFix)}”</b> · `:"")+`${l.length} ${l.length===1?"produto":"produtos"} na loja ${STORES[S.store].code}`;
  renderFilters();
  if(l.length){$("#grid").innerHTML=l.map((p,i)=>card(p,Math.min(i,12)*45)).join("");return}
  if(base.length){$("#grid").innerHTML=`<div class="alt" style="grid-column:1/-1"><img src="${IMG.smiley}" alt=""><b>Nenhum produto com esses filtros.</b><span>Tire um filtro ou limpe todos para ver os ${base.length} produtos.</span><button class="btn btn-dark" data-fclear="1">Limpar filtros</button></div>`;return}
  const sug=POPULAR.slice(0,6);
  $("#grid").innerHTML=`<div class="alt" style="grid-column:1/-1"><img src="${IMG.fumaca}" alt=""><b>Não encontramos “${esc(S.q)}”.</b><span>Confira a grafia ou tente um termo mais simples. Também dá para perguntar no WhatsApp da loja.</span><div class="ac-chips" style="justify-content:center">${sug.map(x=>`<button data-acq="${esc(x)}">${esc(x)}</button>`).join("")}</div></div>`+
    `<div style="grid-column:1/-1"><div class="sec-head" style="margin-top:10px"><h3>Mais <em>vendidos</em></h3></div></div>`+P.filter(p=>p.hl).slice(0,4).map(p=>card(p)).join("");
}
function openFilters(o){$("#filters").classList.toggle("on",o);$("#scrim").classList.toggle("on",o||$("#drawer").classList.contains("on"))}

/* =========================================================
   CHROME / VIEWS
   ========================================================= */
function renderChrome(){
  const st=STORES[S.store];
  $("#pill-code").textContent=st.code;$("#pill-name").textContent=st.name;$("#bn-rating").textContent=st.rating;
  $("#seller-bar").hidden=!S.seller;if(S.seller)$("#seller-name").textContent=S.seller;
  const t=[`<b>Entrega em ${st.city}</b> ${st.eta}`,"<b>#PRIMEIRACOMPRA</b> 5% OFF na primeira compra","<b>Retire na loja</b> sem taxa de entrega",`<b>Aberto até ${hh(st.hrs.wk[1])}</b> de segunda a sábado`,`<b>${st.score} ★ no Google</b> ${st.count} avaliações`,"<b>Tattoo Supply</b> para estúdios e tatuadores","<b>Venda proibida</b> para menores de 18 anos"];
  $("#f-pay").innerHTML=PAY_BRANDS.map(b=>`<span>${b}</span>`).join("");
  $("#f-legal").innerHTML=Object.values(STORES).map(s=>`<b style="color:#c7c9c2">Smoke House ${s.code}</b> · ${esc(s.addr)} · WhatsApp ${s.phoneLabel} · CNPJ ${s.cnpj||'<span style="color:#ff8a8c">a informar</span>'}`).join("<br>");
  const wa=$("#wa-fab");wa.hidden=false;wa.href=`https://api.whatsapp.com/send?phone=${st.phone}&text=${encodeURIComponent(`Olá, Smoke House ${st.code}! Vim pelo site e tenho uma dúvida.`)}`;$("#wa-tip").textContent=`Dúvidas? Fale com a loja ${st.code}`;
  $("#bnav").hidden=false;document.body.classList.add("has-bnav");
  document.querySelectorAll("[data-bn]").forEach(b=>b.classList.toggle("on",(b.dataset.bn==="home"&&S.view==="home")||(b.dataset.bn==="cats"&&S.view==="list"&&!S.q)||(b.dataset.bn==="search"&&S.view==="list"&&!!S.q)));
  if(!ls.get("sh_cookie"))$("#cookie").hidden=false;
  $("#ticker").innerHTML=[...t,...t].map(x=>`<span>✱ ${x}</span>`).join("");
  $("#catbar").innerHTML=`<button class="all" id="all-cats" aria-expanded="false"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M4 6h16M4 12h16M4 18h16"/></svg>Todas categorias</button>`+
    CATS.map(c=>`<button data-go="${c}" class="${S.view==="list"&&S.cat===c&&!S.q?"on":""}">${c}</button>`).join("")+
    `<button class="promo ${S.view==="list"&&S.cat==="promo"?"on":""}" data-go="promo">Ofertas</button>`;
  $("#mega-in").innerHTML="<h6>Todas as categorias</h6>"+[...CATS,"Destaques"].map(c=>`<button data-go="${c}">${c==="Destaques"?"Mais vendidos":c}</button>`).join("");
}
function renderView(){
  $("#home").hidden=S.view!=="home";$("#listing").hidden=S.view!=="list";$("#checkout").hidden=S.view!=="checkout";$("#page").hidden=S.view!=="page";
  if(S.view==="home")renderHome();else if(S.view==="list")renderListing();else if(S.view==="page")renderPage();else renderCheckout();
}
function renderPage(){
  const g=GUIDES.find(x=>x.id===S.page),pg=PAGES[S.page];
  if(g){
    const prods=P.filter(g.prods);
    $("#page").innerHTML=`<article class="page"><div class="crumbs"><button data-home="1">Início</button> / <button data-page="guias">Guias</button> / ${esc(g.title)}</div>
      <span class="kicker">${g.kicker}</span><h1>${g.title}</h1><div class="meta">Leitura de ${g.read} · Equipe Smoke House</div>${g.html}
      <section class="shop"><div class="sec-head"><h3>Produtos deste <em>guia</em></h3><button class="see" data-go="${prods[0]?.cat||"Destaques"}">Ver categoria</button></div><div class="grid">${prods.slice(0,8).map((p,i)=>card(p,i*45)).join("")}</div></section>
      <div class="page-nav">${GUIDES.filter(x=>x.id!==g.id).map(x=>`<button data-guide="${x.id}">Próximo guia: ${x.title}</button>`).join("")}</div></article>`;
  }else if(pg){
    $("#page").innerHTML=`<article class="page"><div class="crumbs"><button data-home="1">Início</button> / ${esc(pg.title)}</div><span class="kicker">${pg.kicker}</span><h1>${pg.title}</h1>${pg.html()}
      ${S.page!=="guias"?`<div class="page-nav">${["entrega","trocas","pagamento","promocoes","privacidade","termos","sobre"].filter(k=>k!==S.page).map(k=>`<button data-page="${k}">${PAGES[k].title}</button>`).join("")}</div>`:""}</article>`;
  }
  observe();
}
function goPage(k){S.view="page";S.page=k;$("#mega").hidden=true;acOpen(false);openCart(false);renderChrome();renderView();window.scrollTo(0,0)}
function renderAll(){renderChrome();renderView();renderCart()}
const toTop=()=>window.scrollTo({top:0,behavior:RM?"auto":"smooth"});
function goCat(c){S.view="list";S.cat=c;S.q="";S.f=newF();$("#q").value="";$("#mega").hidden=true;acOpen(false);renderChrome();renderView();toTop()}
function goHome(){S.view="home";S.q="";$("#q").value="";$("#mega").hidden=true;renderChrome();renderView();toTop()}

/* ---- reveal ---- */
let io=null;
function observe(){
  const els=document.querySelectorAll(".rv:not(.in),.rv-pop:not(.in)");
  if(RM||!("IntersectionObserver" in window)){els.forEach(e=>e.classList.add("in"));return}
  io=io||new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}}),{rootMargin:"0px 0px -40px 0px"});
  els.forEach(e=>io.observe(e));
}

/* =========================================================
   CARRINHO
   ========================================================= */
function totals(co){
  const l=Object.entries(S.cart).map(([id,q])=>({...P.find(p=>p.id==id),q}));
  let sub=0,disc=0;l.forEach(x=>sub+=x.p*x.q);
  const sedas=l.filter(x=>x.cat==="Sedas"&&x.hot).flatMap(x=>Array(x.q).fill(x.p)).sort((a,b)=>a-b);
  for(let i=0;i<Math.floor(sedas.length/3);i++)disc+=sedas[i];
  let fee=0,feeTxt="Grátis",pixDisc=0;
  if(co&&co.tipo==="entrega"){const b=STORES[S.store].bairros.find(x=>x[0]===co.bairro);fee=b?b[1]:0;feeTxt=b?brl(b[1]):co.bairro?"A confirmar":"Escolha o bairro"}
  if(co&&co.pag==="pix")pixDisc=(sub-disc)*0.05;
  return {l,sub,disc,fee,feeTxt,pixDisc,total:sub-disc-pixDisc+fee,pix:(sub-disc)*0.95,count:l.reduce((a,x)=>a+x.q,0)};
}
function renderCart(){
  const t=totals(),st=STORES[S.store];
  $("#cart-n").hidden=!t.count;$("#cart-n").textContent=t.count;$("#bn-n").hidden=!t.count;$("#bn-n").textContent=t.count;$("#cart-sub").textContent=brl(t.sub-t.disc);
  if(!t.l.length){$("#cart-body").innerHTML=`<div class="empty-cart"><img src="${IMG.smiley}" alt="">Seu carrinho está vazio.<br>Adicione produtos da loja ${st.code}.</div>`;$("#cart-foot").innerHTML="";return}
  $("#cart-body").innerHTML=t.l.map(x=>`<div class="line"><div class="mini" style="background:${grad(x.b)}">${tl(x)}</div><div><h5>${esc(x.n)}</h5><small>${brl(x.p)} un.</small></div><div class="qty"><button data-q="${x.id}" data-d="-1" aria-label="Diminuir">−</button><span>${x.q}</span><button data-q="${x.id}" data-d="1" aria-label="Aumentar">+</button></div></div>`).join("");
  $("#cart-foot").innerHTML=`
    <div class="sum"><div><span>Subtotal</span><span>${brl(t.sub)}</span></div>
      ${t.disc?`<div class="disc"><span>Promoção 3 por 2</span><span>-${brl(t.disc)}</span></div>`:""}
      <div><span>Entrega</span><span>calculada no próximo passo</span></div></div>
    <div class="total"><span>Total</span><span>${brl(t.sub-t.disc)}</span></div>
    <p class="note" style="color:var(--green);font-weight:600">${brl(t.pix)} pagando no Pix</p>
    <p class="note">${maxParc(t.sub-t.disc)>1?`ou até ${maxParc(t.sub-t.disc)}x de ${brl((t.sub-t.disc)/maxParc(t.sub-t.disc))} sem juros no cartão · `:""}Pix, crédito, débito, carteira digital, boleto e dinheiro</p>
    <button class="btn btn-green" id="go-co">Finalizar pedido</button>
    <button class="btn btn-line" id="keep" style="color:var(--fg);border-color:var(--line)">Continuar comprando</button>`;
}
function openCart(o){$("#drawer").classList.toggle("on",o);$("#scrim").classList.toggle("on",o)}
function copy(text,ok){const p=navigator.clipboard?.writeText(text);p?p.then(()=>toast(ok),()=>toast("Não foi possível copiar. Selecione o texto e copie.")):toast("Não foi possível copiar. Selecione o texto e copie.")}
function flyToCart(btn){
  const cart=$("#open-cart"),n=$("#cart-n");
  const bump=()=>{n.classList.remove("bump");void n.offsetWidth;n.classList.add("bump");cart.classList.remove("bump");void cart.offsetWidth;cart.classList.add("bump")};
  const th=btn.closest(".card")?.querySelector(".thumb");
  if(RM||!th){bump();return}
  const a=th.getBoundingClientRect(),b=cart.getBoundingClientRect();
  const f=document.createElement("div");f.className="fly";f.style.cssText=`left:${a.left}px;top:${a.top}px;width:${a.width}px;height:${a.height}px;background:${th.style.background}`;
  document.body.appendChild(f);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{f.style.transform=`translate(${b.left+b.width/2-a.left-a.width/2}px,${b.top+b.height/2-a.top-a.height/2}px) scale(.12) rotate(25deg)`;f.style.opacity=".6"}));
  setTimeout(()=>{f.remove();bump()},760);
}
function addToCart(id,btn){const max=getStock(S.store)[id]??0;if((S.cart[id]||0)>=max){toast(`Só temos ${max} em estoque nesta loja`);return}S.cart[id]=(S.cart[id]||0)+1;flyToCart(btn);setTimeout(renderCart,RM?0:700)}

/* =========================================================
   CHECKOUT
   ========================================================= */
function slots(){
  const st=STORES[S.store],d=new Date(),r=d.getDay()===0?st.hrs.sun:st.hrs.wk,open=r[0],close=r[1],h=d.getHours()+d.getMinutes()/60;
  const out=[];if(h>=open&&h<close-.5)out.push("O quanto antes (até 20 min)");
  let s=Math.max(Math.ceil(h+1),Math.ceil(open));for(;s<close&&out.length<5;s++)out.push(`Hoje, ${String(s).padStart(2,"0")}h`);
  if(out.length<3){out.push("Amanhã, 08h","Amanhã, 10h","Amanhã, 14h")}
  return out.slice(0,5);
}
function goCheckout(){
  if(!totals().l.length){toast("Seu carrinho está vazio");return}
  const cli=lsj.get("sh_cli",{});
  S.co={step:cli.nome?2:1,nome:cli.nome||"",whats:cli.whats||"",nasc:cli.nasc||"",tipo:"retirada",slot:null,bairro:"",rua:cli.rua||"",num:cli.num||"",comp:cli.comp||"",ref:"",pag:"pix",troco:"",obs:"",ok18:false,parc:1,err:{}};
  S.co.slot=slots()[0];
  openCart(false);S.view="checkout";renderChrome();renderView();toTop();
}
function age(dmy){const m=dmy.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);if(!m)return -1;const b=new Date(+m[3],+m[2]-1,+m[1]);if(isNaN(b)||b.getDate()!=+m[1])return -1;const n=new Date();let a=n.getFullYear()-b.getFullYear();if(n.getMonth()<b.getMonth()||(n.getMonth()===b.getMonth()&&n.getDate()<b.getDate()))a--;return a}
function mask(v,kind){const d=v.replace(/\D/g,"");if(kind==="tel"){const x=d.slice(0,11);return x.length<3?x:x.length<8?`(${x.slice(0,2)}) ${x.slice(2)}`:`(${x.slice(0,2)}) ${x.slice(2,7)}-${x.slice(7)}`}if(kind==="date"){const x=d.slice(0,8);return x.length<3?x:x.length<5?`${x.slice(0,2)}/${x.slice(2)}`:`${x.slice(0,2)}/${x.slice(2,4)}/${x.slice(4)}`}return v}
const fld=(id,label,val,opts={})=>`<div class="fld ${opts.full?"full":""} ${S.co.err[id]?"err":""}"><label for="co-${id}">${label}</label><input id="co-${id}" data-co="${id}" value="${esc(val)}" ${opts.ph?`placeholder="${opts.ph}"`:""} ${opts.mode?`inputmode="${opts.mode}"`:""} ${opts.mask?`data-mask="${opts.mask}"`:""} autocomplete="${opts.ac||"off"}"><span class="msg-err">${S.co.err[id]||""}</span></div>`;
function coBox(n,title,body,summary){
  const c=S.co,state=c.step===n?"cur":c.step>n?"done":"lock";
  return `<section class="co-box ${state==="cur"?"cur":state==="lock"?"lock":""}"><h3><span>${n}. ${title}</span>${state==="done"?`<button data-costep="${n}">Alterar</button>`:""}</h3>${state==="cur"?body:state==="done"?`<div class="co-sum-txt">${summary}</div>`:""}</section>`;
}
function renderCheckout(){
  const c=S.co,st=STORES[S.store];if(!c){goHome();return}
  if(c.done){renderDone();return}
  const t=totals(c);
  const s1=`<div class="fields">${fld("nome","Nome completo",c.nome,{full:1,ac:"name"})}${fld("whats","WhatsApp",c.whats,{mask:"tel",mode:"tel",ph:"(87) 99999-9999",ac:"tel"})}${fld("nasc","Data de nascimento",c.nasc,{mask:"date",mode:"numeric",ph:"dd/mm/aaaa",ac:"bday"})}</div><p class="note">Usamos a data de nascimento para confirmar a maioridade. O documento com foto é conferido na retirada ou na entrega.</p><button class="btn btn-green" data-conext="1" style="justify-self:start">Continuar</button>`;
  const hasB=st.bairros.length;
  const s2=`<div class="choice">
      <label><input type="radio" name="co-tipo" data-cot="retirada" ${c.tipo==="retirada"?"checked":""}><b>Retirar na loja</b><small>Grátis · ${st.addr?st.addr.split(" · ")[0]:"Loja "+st.code}</small></label>
      <label><input type="radio" name="co-tipo" data-cot="entrega" ${c.tipo==="entrega"?"checked":""}><b>Receber em casa</b><small>${st.eta} · taxa por bairro</small></label>
    </div>
    ${c.tipo==="retirada"?`<div class="fld"><label>Quando você vem buscar?</label><div class="slots">${slots().map(s=>`<label><input type="radio" name="co-slot" data-coslot="${esc(s)}" ${c.slot===s?"checked":""}>${esc(s)}</label>`).join("")}</div></div>`:
    `<div class="fields">
      ${hasB?`<div class="fld full ${c.err.bairro?"err":""}"><label for="co-bairro">Bairro</label><select id="co-bairro" data-co="bairro"><option value="">Selecione o bairro</option>${st.bairros.map(([b,v])=>`<option value="${b}" ${c.bairro===b?"selected":""}>${b} · ${brl(v)}</option>`).join("")}<option value="Outro" ${c.bairro==="Outro"?"selected":""}>Outro bairro · taxa a confirmar</option></select><span class="msg-err">${c.err.bairro||""}</span></div>`:fld("bairro","Bairro (taxa confirmada pela loja)",c.bairro,{full:1})}
      ${fld("rua","Rua",c.rua,{full:1,ac:"address-line1"})}${fld("num","Número",c.num,{mode:"numeric"})}${fld("comp","Complemento",c.comp,{ph:"Apto, bloco"})}${fld("ref","Ponto de referência",c.ref,{full:1,ph:"Opcional"})}
    </div>${hasB?'<p class="note">Taxas por bairro de exemplo. A tabela real vem da loja.</p>':""}`}
    <button class="btn btn-green" data-conext="2" style="justify-self:start">Continuar</button>`;
  const mp=maxParc(t.sub-t.disc);if(c.parc>mp)c.parc=mp;
  const s3=`<div class="choice">${PAYMENTS.map(p=>`<label><input type="radio" name="co-pag" data-cop="${p.k}" ${PAYK(c.pag)===p.k?"checked":""}><b>${p.l}</b><small>${p.desc}</small></label>`).join("")}</div>
    ${PAYK(c.pag)==="credito"?`<div class="fld"><label>Parcelamento</label><div class="slots">${[...Array(mp)].map((_,i)=>`<label><input type="radio" name="co-parc" data-coparc="${i+1}" ${(c.parc||1)===i+1?"checked":""}>${i+1}x de ${brl(t.total/(i+1))}${i?" sem juros":""}</label>`).join("")}</div>${mp===1?'<p class="note">Parcelamento em até 3x sem juros a partir de R$ 60.</p>':""}</div>`:""}
    ${c.pag==="dinheiro"?`<div class="fields">${fld("troco","Troco para quanto?",c.troco,{mode:"decimal",ph:"Ex.: 100"})}</div>`:""}
    <div class="fld"><label for="co-obs">Observações</label><textarea id="co-obs" data-co="obs" rows="2" placeholder="Opcional">${esc(c.obs)}</textarea></div>
    <label class="f-opt ${c.err.ok18?"err":""}" style="align-items:flex-start;${c.err.ok18?"color:var(--hot)":""}"><input type="checkbox" data-co18="1" ${c.ok18?"checked":""} style="margin-top:3px"><span>Confirmo que tenho 18 anos ou mais e vou apresentar documento com foto.</span></label>
    <button class="btn btn-green" data-coconfirm="1" style="justify-self:start">Confirmar pedido · ${brl(t.total)}</button>`;
  const sum1=`${esc(c.nome)} · ${esc(c.whats)}`;
  const sum2=c.tipo==="retirada"?`Retirada na loja ${st.code} · ${esc(c.slot||"")}`:`Entrega em ${esc(c.rua)}, ${esc(c.num)}${c.comp?" · "+esc(c.comp):""} · ${esc(c.bairro)}`;
  $("#checkout").innerHTML=`
    <div class="crumbs"><button data-coback="1">Voltar para a loja</button> / Finalizar pedido</div>
    <div class="co">
      <div>
        <h2>Finalizar pedido</h2>
        <div class="steps">${["Seus dados","Entrega","Pagamento"].map((s,i)=>`<span class="${c.step===i+1?"on":c.step>i+1?"done":""}"><i>${c.step>i+1?"✓":i+1}</i>${s}</span>`).join("")}</div>
        ${coBox(1,"Seus dados",s1,sum1)}
        ${coBox(2,"Entrega ou retirada",s2,sum2)}
        ${coBox(3,"Pagamento",s3,"")}
      </div>
      <aside class="co-aside">
        <h4>Resumo · loja ${st.code}</h4>
        <div class="co-items">${t.l.map(x=>`<div class="line"><div class="mini" style="background:${grad(x.b)}">${tl(x)}</div><div><h5>${esc(x.n)}</h5><small>${x.q} × ${brl(x.p)}</small></div><em>${brl(x.p*x.q)}</em></div>`).join("")}</div>
        <div class="sum">
          <div><span>Subtotal</span><span>${brl(t.sub)}</span></div>
          ${t.disc?`<div class="disc"><span>Promoção 3 por 2</span><span>-${brl(t.disc)}</span></div>`:""}
          ${t.pixDisc?`<div class="disc"><span>Desconto Pix (5%)</span><span>-${brl(t.pixDisc)}</span></div>`:""}
          <div><span>${c.tipo==="entrega"?"Entrega":"Retirada"}</span><span>${c.tipo==="entrega"?t.feeTxt:"Grátis"}</span></div>
        </div>
        <div class="total"><span>Total</span><span>${brl(t.total)}</span></div>
        ${S.seller?`<p class="note">Atendimento: <b style="color:var(--fg)">${esc(S.seller)}</b></p>`:""}
        <button class="btn btn-line" style="color:var(--fg);border-color:var(--line)" data-coedit="1">Editar carrinho</button>
      </aside>
    </div>`;
  const first=$("#checkout .co-box.cur input,#checkout .co-box.cur select");
  if(first&&S.co._focus){first.focus({preventScroll:false});S.co._focus=false}
}
function readCo(){document.querySelectorAll("#checkout [data-co]").forEach(i=>S.co[i.dataset.co]=i.value.trim())}
function validate(step){
  const c=S.co,e={};
  if(step===1){
    if(c.nome.split(" ").filter(Boolean).length<2)e.nome="Digite nome e sobrenome.";
    if(c.whats.replace(/\D/g,"").length<10)e.whats="Digite o WhatsApp com DDD.";
    const a=age(c.nasc);if(a<0)e.nasc="Use o formato dd/mm/aaaa.";else if(a<18)e.nasc="A compra é permitida apenas para maiores de 18 anos.";
  }
  if(step===2&&c.tipo==="entrega"){
    if(!c.bairro)e.bairro="Escolha o bairro.";if(!c.rua)e.rua="Digite a rua.";if(!c.num)e.num="Digite o número.";
  }
  if(step===3){if(!c.ok18)e.ok18=1;if(c.pag==="dinheiro"&&c.troco&&isNaN(parseFloat(c.troco.replace(",","."))))e.troco="Digite só o valor, ex.: 100.";}
  c.err=e;return !Object.keys(e).length;
}
function orderMsg(o){
  const st=STORES[o.store];
  let m=`*Pedido ${o.id}* · Smoke House ${st.code}\n\n*Cliente:* ${o.nome}\n*WhatsApp:* ${o.whats}\n\n*Itens*\n`;
  o.items.forEach(x=>m+=`• ${x.q}x ${x.n} — ${brl(x.p*x.q)}\n`);
  m+=`\nSubtotal: ${brl(o.t.sub)}`;if(o.t.disc)m+=`\nPromoção 3 por 2: -${brl(o.t.disc)}`;if(o.t.pixDisc)m+=`\nDesconto Pix: -${brl(o.t.pixDisc)}`;
  m+=o.tipo==="entrega"?`\nEntrega: ${o.t.feeTxt}\n\n*Endereço:* ${o.rua}, ${o.num}${o.comp?" · "+o.comp:""} · ${o.bairro}${o.ref?"\nReferência: "+o.ref:""}`:`\n\n*Retirada na loja* · ${o.slot}`;
  m+=`\n\n*Total: ${brl(o.t.total)}*\n*Pagamento:* ${payLabel(o,true)}${PAYK(o.pag)==="boleto"?" (enviar boleto)":""}`;
  if(o.obs)m+=`\n*Obs.:* ${o.obs}`;if(o.seller)m+=`\n\n*Colaborador:* ${o.seller}`;
  return m;
}
function confirmOrder(){
  readCo();if(!validate(3)){renderCheckout();return}
  const c=S.co,st=STORES[S.store],t=totals(c);
  const seq=(+ls.get("sh_seq_"+S.store)||1000)+1;ls.set("sh_seq_"+S.store,String(seq));
  const o={id:`${st.code}-${seq}`,store:S.store,at:new Date().toISOString(),items:t.l.map(x=>({id:x.id,n:x.n,p:x.p,q:x.q})),t,seller:S.seller,status:"novo",origem:"site",...Object.fromEntries(["nome","whats","tipo","slot","bairro","rua","num","comp","ref","pag","parc","troco","obs"].map(k=>[k,c[k]]))};
  const orders=lsj.get("sh_orders",[]);orders.unshift(o);lsj.set("sh_orders",orders.slice(0,50));
  lsj.set("sh_cli",{nome:c.nome,whats:c.whats,nasc:c.nasc,rua:c.rua,num:c.num,comp:c.comp});
  S.cart={};S.lastOrder=o;c.done=true;renderCart();renderCheckout();toTop();
}
function renderDone(){
  const o=S.lastOrder,st=STORES[o.store],msg=orderMsg(o);
  $("#checkout").innerHTML=`<div class="done-wrap">
    <div class="done-check"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
    <h2>Pedido registrado!</h2>
    <p class="order-no">Número do pedido <b>${o.id}</b></p>
    <p class="note" style="max-width:46ch">${st.phone?"Envie o pedido pelo WhatsApp da loja para confirmar o pagamento e a "+(o.tipo==="entrega"?"entrega":"retirada")+".":"O WhatsApp da loja LEM ainda não foi cadastrado. Copie o pedido para enviar à loja."}</p>
    <div class="receipt">
      ${o.items.map(x=>`<div><span>${x.q}× ${esc(x.n)}</span><span>${brl(x.p*x.q)}</span></div>`).join("")}
      ${o.t.disc?`<div><span>Promoção 3 por 2</span><span>-${brl(o.t.disc)}</span></div>`:""}
      ${o.t.pixDisc?`<div><span>Desconto Pix</span><span>-${brl(o.t.pixDisc)}</span></div>`:""}
      <div><span>${o.tipo==="entrega"?"Entrega · "+esc(o.bairro):"Retirada · "+esc(o.slot)}</span><span>${o.tipo==="entrega"?o.t.feeTxt:"Grátis"}</span></div>
      <div class="tt"><span>Total · ${payLabel(o)}</span><span>${brl(o.t.total)}</span></div>
    </div>
    <div class="row">
      ${st.phone?`<a class="btn btn-green" target="_blank" rel="noopener" href="https://api.whatsapp.com/send?phone=${st.phone}&text=${encodeURIComponent(msg)}">Enviar pelo WhatsApp</a>`:""}
      <button class="btn btn-line" style="color:var(--fg);border-color:var(--line)" data-copyorder="1">Copiar pedido</button>
      <button class="btn btn-dark" data-coback="1">Voltar para a loja</button>
    </div>
    <p class="note">No sistema final, o pedido entra direto no painel da loja${o.seller?" e gera a comissão de "+esc(o.seller):""}.</p>
  </div>`;
}

/* =========================================================
   EVENTOS
   ========================================================= */
$("#age-yes").onclick=()=>{ls.set("sh_age","ok");route()};
$("#age-no").onclick=()=>{$("#age-denied").hidden=false};
document.querySelectorAll("[data-store]").forEach(b=>b.onclick=()=>{location.hash=b.dataset.store});
$("#switch-store").onclick=()=>{history.replaceState(null,"",location.pathname+location.search);S.store=null;show("v-city")};
$("#go-home").onclick=goHome;$("#crumb-home").onclick=goHome;
$("#search-form").addEventListener("submit",e=>{e.preventDefault();const act=$("#ac .ac-nav.act");if(act&&!$("#ac").hidden){act.click();return}doSearch($("#q").value)});
$("#q").addEventListener("focus",renderAC);
$("#q").addEventListener("input",()=>{clearTimeout(AC.t);AC.t=setTimeout(renderAC,90)});
$("#q").addEventListener("keydown",e=>{
  if(e.key==="ArrowDown"){e.preventDefault();if($("#ac").hidden)renderAC();acMove(1)}
  else if(e.key==="ArrowUp"){e.preventDefault();acMove(-1)}
  else if(e.key==="Escape"){acOpen(false)}
});
$("#sort").addEventListener("change",e=>{S.sort=e.target.value;renderListing()});
$("#f-open").onclick=()=>openFilters(true);
$("#filters").addEventListener("change",e=>{
  const t=e.target,f=S.f;
  if(t.dataset.f){const s=f[t.dataset.f];t.checked?s.add(t.value):s.delete(t.value)}
  else if(t.dataset.fsw)f[t.dataset.fsw]=t.checked;
  else if(t.dataset.fprice!=null)f.price=+t.dataset.fprice;
  renderListing();
});
document.addEventListener("click",e=>{
  const all=e.target.closest("#all-cats");
  if(all){const m=$("#mega");m.hidden=!m.hidden;all.setAttribute("aria-expanded",String(!m.hidden));return}
  if(!e.target.closest("#mega"))$("#mega").hidden=true;
  if(!e.target.closest(".search"))acOpen(false);
  const acq=e.target.closest("[data-acq]");if(acq){doSearch(acq.dataset.acq);return}
  const pid=e.target.closest("[data-pid]");if(pid){const p=P.find(x=>x.id==pid.dataset.pid);doSearch(p.n);return}
  if(e.target.closest("[data-acall]")){doSearch($("#q").value);return}
  const pg=e.target.closest("[data-page]");if(pg){goPage(pg.dataset.page);return}
  const gd=e.target.closest("[data-guide]");if(gd){goPage(gd.dataset.guide);return}
  if(e.target.closest("[data-home]")){goHome();return}
  const ck=e.target.closest("[data-cookie]");if(ck){ls.set("sh_cookie",ck.dataset.cookie);$("#cookie").hidden=true;toast(ck.dataset.cookie==="all"?"Preferência salva: todos os cookies":"Preferência salva: só cookies essenciais");return}
  if(e.target.closest("[data-cookie-reset]")){try{localStorage.removeItem("sh_cookie")}catch(_){}$("#cookie").hidden=false;return}
  const bn=e.target.closest("[data-bn]");if(bn){const k=bn.dataset.bn;
    if(k==="home")goHome();
    else if(k==="cart")openCart(true);
    else if(k==="cats"){window.scrollTo(0,0);$("#mega").hidden=false}
    else if(k==="search"){window.scrollTo(0,0);setTimeout(()=>$("#q").focus(),RM?0:250)}
    return}
  const go=e.target.closest("[data-go]");if(go){goCat(go.dataset.go);return}
  const sg=e.target.closest("[data-store-go]");if(sg){location.hash=sg.dataset.storeGo;return}
  const sc=e.target.closest("[data-scroll]");if(sc){if(S.view!=="home")goHome();setTimeout(()=>$("#"+sc.dataset.scroll).scrollIntoView({behavior:RM?"auto":"smooth"}),60);return}
  const soon=e.target.closest("[data-soon]");if(soon){e.preventDefault();toast(soon.dataset.soon+": próxima etapa do projeto");return}
  const arr=e.target.closest(".s-arrow");if(arr){const sh=arr.parentElement.querySelector(".shelf");sh.scrollBy({left:(arr.classList.contains("s-next")?1:-1)*sh.clientWidth*.8,behavior:"smooth"});return}
  if(e.target.closest("[data-fclear]")){S.f=newF();renderListing();return}
  if(e.target.closest("[data-fprice-clear]")){S.f.price=null;renderListing();return}
  if(e.target.closest("[data-fclose]")){openFilters(false);toTop();return}
  const chip=e.target.closest("[data-chip]");if(chip){const k=chip.dataset.chip,v=chip.dataset.v;if(k==="price")S.f.price=null;else if(k==="avail"||k==="promo")S.f[k]=false;else S.f[k].delete(v);renderListing();return}
  const add=e.target.closest("[data-add]");
  if(add){addToCart(add.dataset.add,add);const txt=add.textContent;add.classList.add("done");add.textContent="Adicionado ✓";setTimeout(()=>{add.classList.remove("done");add.textContent=txt},1300);return}
  /* checkout */
  if(e.target.closest("[data-coback]")){if(S.co&&S.co.done)S.co=null;goHome();return}
  if(e.target.closest("[data-coedit]")){openCart(true);return}
  const cs=e.target.closest("[data-costep]");if(cs){readCo();S.co.step=+cs.dataset.costep;S.co.err={};S.co._focus=true;renderCheckout();return}
  const nx=e.target.closest("[data-conext]");if(nx){readCo();const n=+nx.dataset.conext;if(validate(n)){S.co.step=n+1;S.co._focus=true}renderCheckout();return}
  if(e.target.closest("[data-coconfirm]")){confirmOrder();return}
  if(e.target.closest("[data-copyorder]")){copy(orderMsg(S.lastOrder),"Pedido copiado");return}
});
$("#checkout").addEventListener("input",e=>{const m=e.target.dataset.mask;if(m){const pos=e.target.value.length;e.target.value=mask(e.target.value,m)}});
$("#checkout").addEventListener("change",e=>{
  const t=e.target;readCo();
  if(t.dataset.cot){S.co.tipo=t.dataset.cot;S.co.err={};renderCheckout()}
  else if(t.dataset.coslot){S.co.slot=t.dataset.coslot}
  else if(t.dataset.cop){S.co.pag=t.dataset.cop;S.co.parc=1;renderCheckout()}
  else if(t.dataset.coparc){S.co.parc=+t.dataset.coparc}
  else if(t.dataset.co18){S.co.ok18=t.checked;delete S.co.err.ok18}
  else if(t.id==="co-bairro"&&t.tagName==="SELECT"){renderCheckout()}
});
$("#open-cart").onclick=()=>openCart(true);$("#close-cart").onclick=()=>openCart(false);
$("#scrim").onclick=()=>{openCart(false);openFilters(false)};
$("#drawer").addEventListener("click",e=>{
  const q=e.target.closest("[data-q]");
  if(q){const id=q.dataset.q,d=+q.dataset.d,max=getStock(S.store)[id]??0;if(d>0&&S.cart[id]>=max){toast(`Só temos ${max} em estoque nesta loja`);return}S.cart[id]+=d;if(S.cart[id]<=0)delete S.cart[id];renderCart();if(S.view==="checkout"&&S.co&&!S.co.done){if(!totals().l.length){S.co=null;goHome()}else renderCheckout()}return}
  if(e.target.id==="go-co"){goCheckout();return}
  if(e.target.id==="keep"){openCart(false)}
});
$("#news-form").addEventListener("submit",e=>{e.preventDefault();if(!$("#news-in").value.trim()){toast("Digite seu WhatsApp com DDD");return}$("#news-in").value="";toast("Cadastro feito. Você vai receber as ofertas.")});
addEventListener("scroll",()=>$("#top").classList.toggle("scrolled",scrollY>40),{passive:true});
addEventListener("keydown",e=>{if(e.key==="Escape"){openCart(false);openFilters(false);$("#mega").hidden=true}});

/* ---- banner ---- */
const slides=[...document.querySelectorAll(".slide")];let si=0,timer;
$("#dots").innerHTML=slides.map((_,i)=>`<button aria-label="Banner ${i+1}" class="${i?"":"on"}"><i></i></button>`).join("");
const dots=[...$("#dots").children];
function go(i){slides[si].classList.remove("on");dots[si].classList.remove("on");si=(i+slides.length)%slides.length;slides[si].classList.add("on");void dots[si].offsetWidth;dots[si].classList.add("on");restart()}
function restart(){clearInterval(timer);if(!RM)timer=setInterval(()=>{if(!$("#v-store").hidden&&S.view==="home")go(si+1)},6000)}
dots.forEach((d,i)=>d.onclick=()=>go(i));
$("#h-prev").onclick=()=>go(si-1);$("#h-next").onclick=()=>go(si+1);
restart();

/* ---- fumaça em canvas ---- */
const Smoke=(()=>{
  let cvs=[];let parts=new Map(),raf;
  function size(c){const r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);c.width=r.width*d;c.height=r.height*d;c.getContext("2d").setTransform(d,0,0,d,0,0)}
  function spawn(c){const r=c.getBoundingClientRect();return{x:Math.random()*r.width,y:r.height+40,vx:(Math.random()-.5)*.25,vy:-(.25+Math.random()*.45),s:40+Math.random()*90,life:0,max:500+Math.random()*400,rot:Math.random()*6}}
  function frame(){
    cvs.forEach(c=>{
      if(!c.offsetParent)return;
      const ctx=c.getContext("2d"),r=c.getBoundingClientRect();ctx.clearRect(0,0,r.width,r.height);
      let ps=parts.get(c);if(!ps){ps=[];parts.set(c,ps)}
      const want=c.dataset.smoke==="hero"?14:22;while(ps.length<want)ps.push(Object.assign(spawn(c),{y:Math.random()*r.height}));
      ps.forEach((p,i)=>{p.life++;p.x+=p.vx+Math.sin((p.life+p.rot*50)/90)*.3;p.y+=p.vy;p.s+=.12;
        const k=p.life/p.max,al=(k<.2?k/.2:1-(k-.2)/.8)*(c.dataset.smoke==="hero"?.07:.09);
        const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.s);g.addColorStop(0,`rgba(225,230,220,${al})`);g.addColorStop(1,"rgba(225,230,220,0)");
        ctx.fillStyle=g;ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,7);ctx.fill();
        if(p.life>p.max||p.y<-p.s)ps[i]=spawn(c)});
    });
    raf=requestAnimationFrame(frame);
  }
  function refresh(){if(RM)return;cvs=[...document.querySelectorAll(".smoke-cv")];parts=new Map();cvs.forEach(size);cancelAnimationFrame(raf);raf=requestAnimationFrame(frame)}
  addEventListener("resize",()=>{if(!RM)cvs.forEach(size)});
  document.addEventListener("visibilitychange",()=>{document.hidden?cancelAnimationFrame(raf):refresh()});
  return{refresh};
})();

/* =========================================================
   ÁREA DO VENDEDOR (#colaborador)
   ========================================================= */
const TEAM={
  carla:{name:"Carla",store:"pnz",pin:"1234",goal:2500,cls:""},
  joao:{name:"João",store:"pnz",pin:"1234",goal:2500,cls:"y"},
  bia:{name:"Bia",store:"lem",pin:"1234",goal:2500,cls:"p"}
};
/* link de venda: no protótipo do Claude aponta para o artifact; em qualquer outro host (GitHub Pages, domínio da loja) usa o próprio endereço */
const SITE_URL=/claude\.ai|claudeusercontent|claude\.site/.test(location.hostname)||location.protocol==="file:"?"https://claude.ai/artifact/QdDp8sUNuQNAtzXsiPgX7c":location.href.split("#")[0];
/* comissão: definida pelos donos no painel (commRate) */
const STL={novo:"Novo",confirmado:"Confirmado",separado:"Separado",pronto:"Pronto p/ retirada",a_caminho:"Saiu p/ entrega",concluido:"Concluído",cancelado:"Cancelado"};
const ACT={confirmado:"Confirmar pedido",separado:"Marcar como separado",pronto:"Avisar que está pronto",a_caminho:"Saiu para entrega",concluido:"Concluir pedido"};
const ACTIVE=["novo","confirmado","separado","pronto","a_caminho"];
const BASE_TEAM=JSON.parse(JSON.stringify(TEAM));
function loadTeam(){Object.keys(TEAM).forEach(k=>{if(!BASE_TEAM[k])delete TEAM[k]});Object.assign(TEAM,lsj.get("sh_team",{}));Object.entries(TEAM).forEach(([k,m])=>SELLERS[k]=m.name)}
loadTeam();
const nextSt=o=>({novo:"confirmado",confirmado:"separado",separado:o.tipo==="entrega"?"a_caminho":"pronto",pronto:"concluido",a_caminho:"concluido"})[o.status];
const SV={me:null,tab:"inicio",of:"ativos",open:new Set(),edits:{},sq:"",sf:"todos",sc:"",pos:null,flash:null};

/* ---------- dados compartilhados com a vitrine ---------- */
function seedOrders(){
  if(ls.get("sh_seeded4"))return;
  let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return (seed-1)/2147483646};
  const orders=lsj.get("sh_orders",[]);const now=Date.now();
  Object.entries(TEAM).forEach(([k,m])=>{
    const st=STORES[m.store],stock=getStock(m.store);
    const pool=P.filter(p=>(stock[p.id]??0)>0);
    const dom=new Date().getDate();
    for(let i=0;i<26;i++){
      const daysAgo=i<2?0:i<18?Math.floor(rnd()*Math.max(1,dom-1))+1:dom+Math.floor(rnd()*18),at=new Date(now-daysAgo*864e5-rnd()*8*36e5);
      const items=[];const n=1+Math.floor(rnd()*3);
      for(let j=0;j<n;j++){const p=pool[Math.floor(rnd()*pool.length)];if(!items.find(x=>x.id===p.id))items.push({id:p.id,n:p.n,p:p.p,q:p.p<20?2+Math.floor(rnd()*5):1+Math.floor(rnd()*2)})}
      const sub=items.reduce((a,x)=>a+x.p*x.q,0),tipo=rnd()<.5?"entrega":"retirada",pag=["pix","pix","credito","credito","debito","carteira","dinheiro"][Math.floor(rnd()*7)];
      const b=st.bairros[Math.floor(rnd()*st.bairros.length)],fee=tipo==="entrega"&&b?b[1]:0,pixDisc=pag==="pix"?sub*.05:0;
      const status=daysAgo<1?["novo","confirmado"][i%2]:i===2?"separado":(rnd()<.08?"cancelado":"concluido");
      const seq=(+ls.get("sh_seq_"+m.store)||1000)+1;ls.set("sh_seq_"+m.store,String(seq));
      orders.push({id:`${st.code}-${seq}`,store:m.store,at:at.toISOString(),items,t:{sub,disc:0,pixDisc,fee,feeTxt:fee?brl(fee):"Grátis",total:sub-pixDisc+fee},seller:m.name,
        nome:`Cliente de exemplo ${i+1}`,whats:st.code==="PNZ"?"(87) 90000-00"+String(10+i):"(77) 90000-00"+String(10+i),tipo,slot:"O quanto antes",bairro:b?b[0]:"Centro",rua:"Rua de exemplo",num:String(10+i*7),comp:"",ref:"",pag,troco:"",obs:"",
        status,origem:rnd()<.7?"site":"balcao",paid:status==="concluido"&&daysAgo>12,stockOut:status!=="novo"&&status!=="confirmado",ex:true});
    }
  });
  orders.sort((a,b)=>b.at.localeCompare(a.at));lsj.set("sh_orders",orders);ls.set("sh_seeded4","1");
}
const allOrders=()=>lsj.get("sh_orders",[]).map(o=>(o.status||(o.status="novo"),o));
const saveOrders=os=>lsj.set("sh_orders",os);
function myOrders(){const m=SV.me&&TEAM[SV.me];return m?allOrders().filter(o=>o.store===m.store&&o.seller===m.name):[]}
function unassigned(){const m=TEAM[SV.me];return allOrders().filter(o=>o.store===m.store&&!o.seller&&ACTIVE.includes(o.status))}
function moveStock(o,dir){const st=getStock(o.store);o.items.forEach(x=>{st[x.id]=Math.max(0,(st[x.id]??0)+dir*x.q)});setStock(o.store,st)}
function updOrder(id,fn){const os=allOrders(),o=os.find(x=>x.id===id);if(!o)return null;fn(o);saveOrders(os);return o}

/* ---------- utilidades ---------- */
const fmtWhen=iso=>{const d=new Date(iso),n=new Date(),day=86400000,t=d.toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit"});const dd=Math.floor((new Date(n.toDateString())-new Date(d.toDateString()))/day);return dd===0?`hoje, ${t}`:dd===1?`ontem, ${t}`:d.toLocaleDateString("pt-BR",{day:"2-digit",month:"2-digit"})+`, ${t}`};
const inMonth=iso=>{const d=new Date(iso),n=new Date();return d.getMonth()===n.getMonth()&&d.getFullYear()===n.getFullYear()};
const avatar=(k,extra="")=>`<span class="av ${TEAM[k].cls} ${extra}">${TEAM[k].name[0]}</span>`;
const pill=s=>`<span class="pill st-${s}">${STL[s]}</span>`;
const waLink=(phone,msg)=>`https://api.whatsapp.com/send?phone=55${String(phone).replace(/\D/g,"")}&text=${encodeURIComponent(msg)}`;
function statusMsg(o){
  const st=STORES[o.store],first=o.nome.split(" ")[0];
  const m={novo:`recebemos seu pedido ${o.id}. Já vou conferir tudo por aqui.`,confirmado:`seu pedido ${o.id} está confirmado! Total de ${brl(o.t.total)}.${PAYK(o.pag)==="pix"?" Vou te mandar o QR code do Pix agora.":PAYK(o.pag)==="boleto"?" Vou te mandar o boleto agora.":PAYK(o.pag)==="credito"&&o.tipo==="entrega"?" Se preferir pagar antes, te mando o link do cartão.":""}`,separado:`seu pedido ${o.id} já está separado.`,
    pronto:`seu pedido ${o.id} está pronto para retirada na Smoke House ${st.code}, ${st.short}. Traga um documento com foto.`,a_caminho:`seu pedido ${o.id} saiu para entrega! Tenha um documento com foto em mãos.`,concluido:`obrigado pela compra! Qualquer coisa, é só chamar aqui.`,cancelado:`seu pedido ${o.id} foi cancelado. Se precisar, estou à disposição.`};
  return `Olá, ${first}! Aqui é ${TEAM[SV.me].name}, da Smoke House ${st.code}. ${m[o.status]}`;
}

/* ---------- login ---------- */
function svLogin(){
  const pick=SV.pick||null;
  $("#v-seller").innerHTML=`<div class="sv-login"><canvas class="smoke-cv" data-smoke="sv"></canvas><div class="wrap"><div class="card-l">
    <img class="lg" src="${IMG.logo}" alt="Smoke House">
    <h1>Área do <em>colaborador</em></h1>
    <p>Escolha seu nome e digite o PIN de 4 dígitos.</p>
    <div class="who">${Object.entries(TEAM).map(([k,m])=>`<button data-svwho="${k}" class="${pick===k?"on":""}">${avatar(k)}<b>${m.name}</b><small>Loja ${STORES[m.store].code}</small></button>`).join("")}</div>
    ${pick?`<div class="pin" id="pin">${[0,1,2,3].map(i=>`<input inputmode="numeric" maxlength="1" type="password" aria-label="Dígito ${i+1} do PIN" data-pin="${i}">`).join("")}</div><span class="hint">Protótipo: o PIN de todos os colaboradores é 1234.</span>`:""}
    <button class="back" data-svexit="1">Voltar para a loja</button>
  </div></div></div>`;
  if(pick)setTimeout(()=>{if(document.activeElement?.dataset?.pin==null)$("[data-pin='0']")?.focus()},50);
  Smoke.refresh();
}

/* ---------- casca ---------- */
function svShell(){
  const m=TEAM[SV.me],st=STORES[m.store],mine=myOrders();
  const newN=mine.filter(o=>o.status==="novo").length+unassigned().length;
  const low=P.filter(p=>{const q=getStock(m.store)[p.id]??0;return q<MIN_STOCK}).length;
  const tabs=[["inicio","Início"],["pedidos","Pedidos",newN],["estoque","Estoque",low],["link","Meu link"],["comissoes","Comissões"]];
  $("#v-seller").innerHTML=`<header class="sv-top"><div class="wrap">
      <img src="${IMG.logo}" alt="Smoke House"><span class="tag-s">Área do colaborador · ${st.code}</span>
      <div class="me">${avatar(SV.me)}<span class="t"><b>${m.name}</b><small>Loja ${st.name}</small></span>
      <button class="ghost" data-svstore="1">Ver loja</button><button class="ghost" data-svout="1">Sair</button></div>
    </div>
    <nav class="sv-tabs"><div class="wrap">${tabs.map(([k,l,c])=>`<button data-svtab="${k}" class="${SV.tab===k?"on":""}">${l}${c?`<span class="cnt">${c}</span>`:""}</button>`).join("")}</div></nav></header>
    <main class="wrap sv-main" id="sv-main"></main>`;
  ({inicio:svHome,pedidos:svOrders,estoque:svStock,link:svLink,comissoes:svComm})[SV.tab]();
}

/* ---------- início ---------- */
function svHome(){
  const m=TEAM[SV.me],mine=myOrders(),valid=mine.filter(o=>o.status!=="cancelado");
  const month=valid.filter(o=>inMonth(o.at)),done=month.filter(o=>o.status==="concluido");
  const salesM=month.reduce((a,o)=>a+o.t.total,0),doneM=done.reduce((a,o)=>a+o.t.total,0);
  const commRec=mine.filter(o=>o.status==="concluido"&&!o.paid).reduce((a,o)=>a+o.t.total*commRate(),0);
  const ticket=month.length?salesM/month.length:0,goal=goalOf(SV.me),pct=Math.min(100,salesM/goal*100);
  const h=new Date().getHours(),hi=h<12?"Bom dia":h<18?"Boa tarde":"Boa noite";
  const act=mine.filter(o=>ACTIVE.includes(o.status)).slice(0,5),un=unassigned();
  const stock=getStock(m.store),low=P.map(p=>({p,q:stock[p.id]??0})).filter(x=>x.q<MIN_STOCK).sort((a,b)=>a.q-b.q).slice(0,5);
  /* ranking da loja */
  const rank=Object.entries(TEAM).filter(([k,t])=>t.store===m.store).map(([k,t])=>({k,v:allOrders().filter(o=>o.seller===t.name&&o.store===t.store&&o.status!=="cancelado"&&inMonth(o.at)).reduce((a,o)=>a+o.t.total,0)})).sort((a,b)=>b.v-a.v);
  /* gráfico 14 dias */
  const days=[...Array(14)].map((_,i)=>{const d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()-13+i);return d});
  const vals=days.map(d=>valid.filter(o=>new Date(o.at).toDateString()===d.toDateString()).reduce((a,o)=>a+o.t.total,0));
  const mx=Math.max(50,...vals),step=mx>400?200:mx>200?100:50,top=Math.ceil(mx/step)*step;
  const W=560,H=170,pl=40,pb=22,bw=(W-pl)/14;
  const grid=[0,top/2,top].map(v=>{const y=H-pb-(v/top)*(H-pb-10);return `<line class="gl" x1="${pl}" x2="${W}" y1="${y}" y2="${y}"/><text x="${pl-6}" y="${y+3}" text-anchor="end">${v>=1000?(v/1000).toFixed(1).replace(".",",")+" mil":Math.round(v)}</text>`}).join("");
  const bars=vals.map((v,i)=>{const bh=(v/top)*(H-pb-10),x=pl+i*bw+4;return `<rect class="bar" x="${x}" y="${H-pb-bh}" width="${bw-8}" height="${Math.max(bh,v?2:0)}" rx="3"><title>${days[i].toLocaleDateString("pt-BR")}: ${brl(v)}</title></rect>${i%2===1||i===13?`<text x="${x+(bw-8)/2}" y="${H-6}" text-anchor="middle">${days[i].getDate()}/${days[i].getMonth()+1}</text>`:""}`}).join("");
  $("#sv-main").innerHTML=`<div class="sv-h"><div><h2>${hi}, <em>${m.name}</em></h2><p>Seu resumo de ${new Date().toLocaleDateString("pt-BR",{month:"long"})} na loja ${STORES[m.store].code}.</p></div>${mine.some(o=>o.ex)?'<span class="ex-note">Inclui pedidos de exemplo</span>':""}</div>
    <div class="kpis">
      <div class="kpi dark"><span>Vendas no mês</span><b>${brl(salesM)}</b><small>${month.length} pedidos · ${brl(doneM)} concluídos</small></div>
      <div class="kpi"><span>Comissão a receber</span><b>${brl(commRec)}</b><small>${Math.round(commRate()*100)}% sobre pedidos concluídos</small></div>
      <div class="kpi"><span>Pedidos em andamento</span><b>${mine.filter(o=>ACTIVE.includes(o.status)).length}</b><small>${(n=>n===1?"1 novo aguardando você":n+" novos aguardando você")(mine.filter(o=>o.status==="novo").length)}</small></div>
      <div class="kpi"><span>Ticket médio</span><b>${brl(ticket)}</b><small>no mês</small></div>
    </div>
    <div class="sv-grid">
      <div style="display:grid;gap:16px;min-width:0">
        <div class="panel"><h3>Meta do mês <span style="font-weight:500;font-size:12.5px;color:var(--muted)">${Math.round(pct)}%</span></h3>
          <div class="goal-bar"><i id="goal-i"></i></div>
          <div class="goal-txt"><span><b>${brl(salesM)}</b> de ${brl(goal)}</span><span>${salesM>=goal?"Meta batida! 🎉":"Faltam "+brl(goal-salesM)}</span></div></div>
        <div class="panel chart"><h3>Vendas dos últimos 14 dias</h3><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Vendas por dia">${grid}${bars}</svg></div>
        <div class="panel"><h3>Precisam de você <button data-svtab="pedidos">Ver pedidos</button></h3>
          <div class="mini-list">${un.length?`<button class="mini-row" data-svtab="pedidos" data-svof="sem"><span><b>${un.length} ${un.length>1?"pedidos":"pedido"} da loja sem atendente</b><small>Assuma para atender e ganhar a comissão</small></span>${pill("novo")}</button>`:""}
          ${act.length?act.map(o=>`<button class="mini-row" data-svopen="${o.id}"><span><b>${o.id} · ${esc(o.nome)}</b><small>${fmtWhen(o.at)} · ${o.tipo==="entrega"?"Entrega":"Retirada"} · ${brl(o.t.total)}</small></span>${pill(o.status)}</button>`).join(""):(!un.length?'<p class="note">Nenhum pedido em andamento. Compartilhe seu link para vender mais.</p>':"")}</div></div>
      </div>
      <div style="display:grid;gap:16px;min-width:0">
        <div class="panel"><h3>Suas tarefas <span style="font-weight:500;font-size:12px;color:var(--muted)">enviadas pelos donos</span></h3><div class="tasks">${tasks().filter(x=>x.who===SV.me).map(x=>`<label class="task ${x.done?"dn":""}"><input type="checkbox" data-svtask="${x.id}" ${x.done?"checked":""}><span>${esc(x.text)}</span></label>`).join("")||'<p class="note">Nenhuma tarefa por enquanto.</p>'}</div></div>
        <div class="panel"><h3>Ranking da loja ${STORES[m.store].code}</h3><div class="rank">${rank.map((r,i)=>`<div class="${r.k===SV.me?"me":""}"><em>${i+1}º</em>${avatar(r.k)}<span>${TEAM[r.k].name}${r.k===SV.me?" (você)":""}</span><b>${brl(r.v)}</b></div>`).join("")}</div></div>
        <div class="panel"><h3>Estoque baixo <button data-svtab="estoque" data-svsf="baixo">Ver estoque</button></h3>
          <div class="mini-list">${low.length?low.map(x=>`<div class="mini-row"><span><b>${esc(x.p.n)}</b><small>${x.p.cat}</small></span><span class="pill ${x.q?"warnp":"lowp"}">${x.q?x.q+" un.":"Esgotado"}</span></div>`).join(""):'<p class="note">Tudo abastecido.</p>'}</div></div>
        <div class="panel" style="background:var(--green);color:#fff;border-color:var(--green)"><h3 style="color:#fff">Seu link de venda</h3><p style="margin:0;font-size:13px;opacity:.9">Cada pedido feito pelo seu link conta para a sua meta e gera comissão.</p><button class="btn btn-yellow btn-sm" data-svtab="link" style="justify-self:start">Copiar meu link</button></div>
      </div>
    </div>`;
  requestAnimationFrame(()=>requestAnimationFrame(()=>{const g=$("#goal-i");if(g)g.style.width=pct+"%"}));
}

/* ---------- pedidos ---------- */
function svOrders(){
  const mine=myOrders(),un=unassigned();
  const groups={ativos:["Em andamento",mine.filter(o=>ACTIVE.includes(o.status))],sem:["Sem atendente",un],concluidos:["Concluídos",mine.filter(o=>o.status==="concluido")],cancelados:["Cancelados",mine.filter(o=>o.status==="cancelado")],todos:["Todos",mine]};
  const list=groups[SV.of][1];
  $("#sv-main").innerHTML=`<div class="sv-h"><div><h2>Seus <em>pedidos</em></h2><p>Pedidos feitos pelo seu link e vendas registradas no balcão.</p></div><button class="btn btn-green btn-sm" data-svpos="1">+ Venda no balcão</button></div>
    <div class="chips-st">${Object.entries(groups).map(([k,[l,a]])=>`<button data-svof="${k}" class="${SV.of===k?"on":""}">${l} <em>${a.length}</em></button>`).join("")}</div>
    <div class="orders">${list.length?list.map(o=>svOrderCard(o,SV.of==="sem")).join(""):`<div class="alt"><img src="${IMG.smiley}" alt=""><b>Nada por aqui.</b><span>${SV.of==="sem"?"Nenhum pedido da loja esperando atendente.":"Os pedidos aparecem aqui assim que alguém compra pelo seu link."}</span></div>`}</div>`;
  if(SV.flash){const el=document.querySelector(`[data-oid="${SV.flash}"]`);el?.classList.add("flash");el?.scrollIntoView({block:"center",behavior:RM?"auto":"smooth"});SV.flash=null}
}
function svOrderCard(o,claim){
  const open=SV.open.has(o.id),nx=nextSt(o);
  const flow=["novo","confirmado","separado",o.tipo==="entrega"?"a_caminho":"pronto","concluido"],cur=flow.indexOf(o.status);
  const qn=o.items.reduce((a,x)=>a+x.q,0);
  return `<article class="order" data-oid="${o.id}">
    <button class="o-head" data-svtoggle="${o.id}" aria-expanded="${open}">
      <span class="l"><span class="id">${o.id} ${o.ex?'<small>exemplo</small>':""} <small>${o.origem==="balcao"?"Balcão":"Site"}</small></span><span class="sub">${esc(o.nome)} · ${fmtWhen(o.at)} · ${qn} ${qn>1?"itens":"item"} · ${o.tipo==="entrega"?"Entrega":"Retirada"}</span></span>
      <span class="r">${pill(o.status)}<b>${brl(o.t.total)}</b></span>
    </button>
    ${open?`<div class="o-body">
      ${o.status!=="cancelado"?`<div class="timeline">${flow.map((s,i)=>`<span class="${i<=cur?"d":""}"><i></i>${STL[s].replace(" p/ retirada","").replace(" p/ entrega","")}</span>`).join("")}</div>`:""}
      <div class="o-items">${o.items.map(x=>`<div><span>${x.q}× ${esc(x.n)}</span><span>${brl(x.p*x.q)}</span></div>`).join("")}
        ${o.t.disc?`<div style="color:var(--green)"><span>Promoção 3 por 2</span><span>-${brl(o.t.disc)}</span></div>`:""}${o.t.pixDisc?`<div style="color:var(--green)"><span>Desconto Pix</span><span>-${brl(o.t.pixDisc)}</span></div>`:""}
        ${o.tipo==="entrega"?`<div><span>Entrega</span><span>${o.t.feeTxt}</span></div>`:""}<div style="font-weight:800"><span>Total</span><span>${brl(o.t.total)}</span></div></div>
      <div class="o-meta">
        <div><span>Cliente</span>${esc(o.nome)}<br>${esc(o.whats||"—")}</div>
        <div><span>${o.tipo==="entrega"?"Endereço":"Retirada"}</span>${o.tipo==="entrega"?`${esc(o.rua)}, ${esc(o.num)}${o.comp?" · "+esc(o.comp):""}<br>${esc(o.bairro)}${o.ref?" · "+esc(o.ref):""}`:esc(o.slot||"Na loja")}</div>
        <div><span>Pagamento</span>${esc(payLabel(o,true))}</div>
        <div><span>Sua comissão</span>${o.status==="cancelado"?"—":brl(o.t.total*commRate())+(o.status==="concluido"?(o.paid?" · paga":" · a receber"):" · prevista")}</div>
        ${o.obs?`<div style="grid-column:1/-1"><span>Observações</span>${esc(o.obs)}</div>`:""}
      </div>
      <div class="o-actions">
        ${claim?`<button class="btn btn-green" data-svclaim="${o.id}">Assumir este pedido</button>`:""}
        ${!claim&&nx?`<button class="btn btn-green" data-svadv="${o.id}">${ACT[nx]}</button>`:""}
        ${o.whats&&!claim?`<a class="btn btn-dark" target="_blank" rel="noopener" href="${waLink(o.whats,statusMsg(o))}">Avisar no WhatsApp</a>`:""}
        ${!claim&&ACTIVE.includes(o.status)?`<button class="btn btn-line" style="color:var(--hot)" data-svcancel="${o.id}">Cancelar</button>`:""}
      </div>
    </div>`:""}
  </article>`;
}

/* ---------- estoque ---------- */
function svStock(){
  const m=TEAM[SV.me],stock=getStock(m.store),q=norm(SV.sq);
  let rows=P.map(p=>({p,q:SV.edits[p.id]??stock[p.id]??0,orig:stock[p.id]??0}));
  if(q)rows=rows.filter(r=>r.p._h.includes(q));
  if(SV.sc)rows=rows.filter(r=>r.p.cat===SV.sc);
  if(SV.sf==="baixo")rows=rows.filter(r=>r.q<MIN_STOCK&&r.q>0);
  if(SV.sf==="esgotado")rows=rows.filter(r=>r.q<=0);
  const nCh=Object.keys(SV.edits).length;
  const all=P.map(p=>stock[p.id]??0),nLow=all.filter(v=>v>0&&v<MIN_STOCK).length,nOut=all.filter(v=>v<=0).length;
  $("#sv-main").innerHTML=`<div class="sv-h"><div><h2>Estoque <em>${STORES[m.store].code}</em></h2><p>O que você salvar aqui aparece na hora na vitrine da loja ${STORES[m.store].code}. Estoque mínimo: ${MIN_STOCK} unidades.</p></div></div>
    <div class="chips-st">${[["todos","Todos",P.length],["baixo","Estoque baixo",nLow],["esgotado","Esgotados",nOut]].map(([k,l,c])=>`<button data-svsf="${k}" class="${SV.sf===k?"on":""}">${l} <em>${c}</em></button>`).join("")}</div>
    <div class="stock-tools"><input id="sv-sq" type="search" placeholder="Buscar produto" value="${esc(SV.sq)}" aria-label="Buscar produto no estoque"><select id="sv-sc" aria-label="Categoria"><option value="">Todas as categorias</option>${CATS.map(c=>`<option ${SV.sc===c?"selected":""}>${c}</option>`).join("")}</select></div>
    <div class="tbl-wrap"><table class="stock"><thead><tr><th>Produto</th><th>Preço</th><th>Quantidade</th><th>Situação</th></tr></thead><tbody>
    ${rows.length?rows.map(r=>`<tr class="${SV.edits[r.p.id]!=null?"chg":""}"><td><div class="pn"><span class="mini" style="background:${grad(r.p.b)}">${tl(r.p)}</span><span><b>${esc(r.p.n)}</b><br><small style="color:var(--muted)">${r.p.cat}</small></span></div></td>
      <td style="font-variant-numeric:tabular-nums">${brl(r.p.p)}</td>
      <td><span class="qctl"><button data-svq="${r.p.id}" data-d="-1" aria-label="Diminuir">−</button><input data-svqi="${r.p.id}" value="${r.q}" inputmode="numeric" aria-label="Quantidade de ${esc(r.p.n)}"><button data-svq="${r.p.id}" data-d="1" aria-label="Aumentar">+</button></span>${SV.edits[r.p.id]!=null?`<small style="margin-left:8px;color:var(--muted)">antes ${r.orig}</small>`:""}</td>
      <td>${r.q<=0?'<span class="pill lowp">Esgotado</span>':r.q<MIN_STOCK?'<span class="pill warnp">Baixo</span>':'<span class="pill okp">Ok</span>'}</td></tr>`).join(""):`<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:30px">Nenhum produto com esse filtro.</td></tr>`}
    </tbody></table></div>
    ${nCh?`<div class="savebar"><span><b>${nCh}</b> ${nCh>1?"produtos alterados":"produto alterado"}</span><div class="row"><button class="btn btn-line btn-sm" style="color:#fff;border-color:#3d403b" data-svundo="1">Desfazer</button><button class="btn btn-yellow btn-sm" data-svsave="1">Salvar estoque</button></div></div>`:""}`;
}

/* ---------- meu link ---------- */
function svLink(){
  const m=TEAM[SV.me],st=STORES[m.store],url=SITE_URL+`#${m.store}-vendedor-${SV.me}`;
  const mine=myOrders().filter(o=>o.origem==="site"&&o.status!=="cancelado");
  const tpls=[["Para clientes no WhatsApp",`Oi! Aqui é ${m.name}, da Smoke House ${st.code}. Agora você pode ver o estoque e fazer seu pedido pelo site, com entrega ou retirada na loja:\n${url}`],
    ["Para o status do Instagram",`Sedas, isqueiros, Tattoo Supply e muito mais. Peça pelo meu link e retire na loja ou receba em casa 👇\n${url}`],
    ["Para tatuadores",`Oi! Aqui é ${m.name}, da Smoke House ${st.code}. A linha Tattoo Supply está no site: confere o estoque e pede por aqui que eu separo pra você:\n${url}`]];
  $("#sv-main").innerHTML=`<div class="sv-h"><div><h2>Meu <em>link</em></h2><p>Todo pedido feito por este link fica registrado no seu nome e gera ${Math.round(commRate()*100)}% de comissão.</p></div></div>
    <div class="sv-grid">
      <div style="display:grid;gap:16px;min-width:0">
        <div class="panel"><h3>Seu link de venda</h3><div class="link-box"><input id="sv-url" readonly value="${esc(url)}" aria-label="Seu link"><button class="btn btn-green" data-svcopy="${esc(url)}">Copiar link</button></div>
          <div class="kpis" style="grid-template-columns:repeat(2,1fr)"><div class="kpi"><span>Pedidos pelo link</span><b>${mine.length}</b><small>desde o início</small></div><div class="kpi"><span>Vendas pelo link</span><b>${brl(mine.reduce((a,o)=>a+o.t.total,0))}</b><small>pedidos não cancelados</small></div></div></div>
        <div class="panel"><h3>Mensagens prontas</h3><div class="tpl">${tpls.map(([t,x])=>`<div><b class="t">${t}</b><p>${esc(x)}</p><button class="btn btn-dark btn-sm" style="justify-self:start" data-svcopy="${esc(x)}">Copiar mensagem</button></div>`).join("")}</div></div>
      </div>
      <div class="qr-wrap"><b style="font-family:var(--brush);font-weight:400;font-size:28px">QR do balcão</b><div id="qr"></div><small>Imprima e deixe no caixa: o cliente aponta a câmera e compra pelo seu link.</small></div>
    </div>`;
  try{if(window.QRCode)new QRCode($("#qr"),{text:url,width:360,height:360,colorDark:"#0e0f0d",colorLight:"#ffffff",correctLevel:QRCode.CorrectLevel.M});else $("#qr").innerHTML='<p style="color:var(--ink);font-size:12px;margin:0;max-width:180px">O QR code aparece quando a página termina de carregar.</p>'}catch(e){}
}

/* ---------- comissões ---------- */
function svComm(){
  const mine=myOrders().filter(o=>o.status!=="cancelado");
  const rec=mine.filter(o=>o.status==="concluido"&&!o.paid),paid=mine.filter(o=>o.paid),prev=mine.filter(o=>ACTIVE.includes(o.status));
  const s=a=>a.reduce((x,o)=>x+o.t.total*commRate(),0);
  $("#sv-main").innerHTML=`<div class="sv-h"><div><h2>Suas <em>comissões</em></h2><p>Taxa de ${Math.round(commRate()*100)}% sobre o total dos pedidos concluídos. Os donos fecham e pagam pelo painel deles.</p></div></div>
    <div class="kpis">
      <div class="kpi dark"><span>A receber</span><b>${brl(s(rec))}</b><small>${rec.length} pedidos concluídos</small></div>
      <div class="kpi"><span>Prevista</span><b>${brl(s(prev))}</b><small>${prev.length} pedidos em andamento</small></div>
      <div class="kpi"><span>Já paga</span><b>${brl(s(paid))}</b><small>${paid.length} pedidos</small></div>
      <div class="kpi"><span>Total no mês</span><b>${brl(s(mine.filter(o=>inMonth(o.at)&&o.status==="concluido")))}</b><small>concluídos no mês</small></div>
    </div>
    <div class="panel" style="margin-top:16px"><h3>Extrato</h3><div style="overflow-x:auto"><table class="ext"><thead><tr><th>Data</th><th>Pedido</th><th>Cliente</th><th class="num">Valor</th><th class="num">Comissão</th><th>Situação</th></tr></thead><tbody>
      ${mine.map(o=>`<tr><td>${new Date(o.at).toLocaleDateString("pt-BR")}</td><td><b>${o.id}</b></td><td>${esc(o.nome)}</td><td class="num">${brl(o.t.total)}</td><td class="num"><b>${brl(o.t.total*commRate())}</b></td><td>${o.paid?'<span class="pill okp">Paga</span>':o.status==="concluido"?'<span class="pill warnp">A receber</span>':'<span class="pill st-confirmado">Prevista</span>'}</td></tr>`).join("")||'<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:24px">Sem comissões ainda.</td></tr>'}
    </tbody></table></div></div>`;
}

/* ---------- venda no balcão ---------- */
function svPos(){
  const p=SV.pos,m=TEAM[SV.me],stock=getStock(m.store),q=norm(p.q||"");
  const res=(q?search(p.q).res:P.filter(x=>x.hl)).slice(0,8);
  const tot=p.items.reduce((a,x)=>a+x.p*x.q,0);
  let md=$("#sv-modal");if(!md){md=document.createElement("div");md.id="sv-modal";md.className="modal";document.body.appendChild(md)}
  md.innerHTML=`<div class="modal-box" role="dialog" aria-label="Venda no balcão"><h3>Venda no balcão<button data-svposclose="1" aria-label="Fechar">×</button></h3>
    <div class="fld"><label for="pos-q">Buscar produto</label><input id="pos-q" value="${esc(p.q||"")}" placeholder="Digite o nome, marca ou categoria" autocomplete="off"></div>
    <div class="pos-results">${res.map(x=>{const s=stock[x.id]??0;return `<button data-posadd="${x.id}" ${s<=0?"disabled":""}><span class="mini" style="background:${grad(x.b)}">${tl(x)}</span><span>${esc(x.n)}<br><small style="color:var(--muted)">${s} em estoque</small></span><b>${brl(x.p)}</b></button>`}).join("")||'<p class="note">Nenhum produto encontrado.</p>'}</div>
    <div class="pos-cart">${p.items.map(x=>`<div><span>${x.q}× ${esc(x.n)}</span><span style="display:flex;gap:8px;align-items:center"><b>${brl(x.p*x.q)}</b><button class="x" style="background:var(--line);color:var(--fg);width:26px;height:26px;font-size:14px" data-posrem="${x.id}" aria-label="Remover">×</button></span></div>`).join("")||'<p class="note">Adicione os produtos vendidos.</p>'}</div>
    <div class="fields"><div class="fld"><label for="pos-n">Cliente (opcional)</label><input id="pos-n" value="${esc(p.nome||"")}" placeholder="Nome"></div><div class="fld"><label for="pos-w">WhatsApp (opcional)</label><input id="pos-w" value="${esc(p.whats||"")}" placeholder="(87) 99999-9999" inputmode="tel"></div>
    <div class="fld full"><label for="pos-pag">Pagamento</label><select id="pos-pag">${PAYMENTS.map(x=>`<option value="${x.k}" ${PAYK(p.pag)===x.k?"selected":""}>${x.l}</option>`).join("")}</select></div></div>
    <div class="total"><span>Total</span><span>${brl(tot)}</span></div>
    <button class="btn btn-green" data-posok="1" ${p.items.length?"":"disabled"}>Registrar venda · ${brl(tot)}</button>
    <p class="note">A venda entra como concluída, baixa o estoque e conta para a sua comissão.</p></div>`;
}
function readPos(){const p=SV.pos;p.q=$("#pos-q")?.value||"";p.nome=$("#pos-n")?.value||"";p.whats=$("#pos-w")?.value||"";p.pag=$("#pos-pag")?.value||"pix"}
function closePos(){SV.pos=null;$("#sv-modal")?.remove()}

/* ---------- navegação ---------- */
function renderSV(){
  seedOwner();
  if(!SV.me)SV.me=ls.get("sh_sv_me")||null;
  if(SV.me&&!TEAM[SV.me])SV.me=null;
  seedOrders();
  SV.me?svShell():svLogin();
}
document.addEventListener("click",e=>{
  if($("#v-seller").hidden&&!e.target.closest("#sv-modal")&&!e.target.closest("[data-sv]"))return;
  const t=e.target;
  if(t.closest("[data-sv]")){location.hash="colaborador";return}
  const who=t.closest("[data-svwho]");if(who){SV.pick=who.dataset.svwho;svLogin();return}
  if(t.closest("[data-svexit]")){location.hash=ls.get("sh_age")==="ok"?"pnz":"";return}
  if(t.closest("[data-svout]")){SV.me=null;SV.pick=null;try{localStorage.removeItem("sh_sv_me")}catch(_){}svLogin();return}
  if(t.closest("[data-svstore]")){const m=TEAM[SV.me];ls.set("sh_age","ok");location.hash=`${m.store}-vendedor-${SV.me}`;return}
  const tab=t.closest("[data-svtab]");if(tab){SV.tab=tab.dataset.svtab;const of=tab.dataset.svof,sf=tab.dataset.svsf;if(of)SV.of=of;if(sf)SV.sf=sf;svShell();window.scrollTo(0,0);return}
  const op=t.closest("[data-svopen]");if(op){SV.tab="pedidos";SV.of="ativos";SV.open.add(op.dataset.svopen);SV.flash=op.dataset.svopen;svShell();return}
  const of=t.closest("[data-svof]");if(of){SV.of=of.dataset.svof;svOrders();return}
  const tg=t.closest("[data-svtoggle]");if(tg){const id=tg.dataset.svtoggle;SV.open.has(id)?SV.open.delete(id):SV.open.add(id);svOrders();return}
  const adv=t.closest("[data-svadv]");if(adv){const o=updOrder(adv.dataset.svadv,o=>{const n=nextSt(o);if(n==="separado"&&!o.stockOut){moveStock(o,-1);o.stockOut=true}o.status=n});SV.flash=o.id;svShell();toast(`${o.id}: ${STL[o.status]}`);return}
  const cl=t.closest("[data-svclaim]");if(cl){const o=updOrder(cl.dataset.svclaim,o=>{o.seller=TEAM[SV.me].name});SV.of="ativos";SV.open.add(o.id);SV.flash=o.id;svShell();toast(`Pedido ${o.id} agora é seu`);return}
  const cc=t.closest("[data-svcancel]");if(cc){const id=cc.dataset.svcancel;if(cc.dataset.sure!=="1"){cc.dataset.sure="1";cc.textContent="Confirmar cancelamento";cc.style.background="var(--hot)";cc.style.color="#fff";cc.style.borderColor="var(--hot)";return}
    const o=updOrder(id,o=>{if(o.stockOut){moveStock(o,1);o.stockOut=false}o.status="cancelado"});svShell();toast(`${o.id} cancelado. O estoque foi devolvido.`);return}
  const sf=t.closest("[data-svsf]");if(sf){SV.sf=sf.dataset.svsf;svStock();return}
  const sq=t.closest("[data-svq]");if(sq){const id=sq.dataset.svq,st=getStock(TEAM[SV.me].store),cur=SV.edits[id]??st[id]??0,v=Math.max(0,cur+(+sq.dataset.d));if(v===(st[id]??0))delete SV.edits[id];else SV.edits[id]=v;svStock();return}
  if(t.closest("[data-svundo]")){SV.edits={};svStock();return}
  if(t.closest("[data-svsave]")){const s=TEAM[SV.me].store,st=getStock(s);Object.entries(SV.edits).forEach(([id,v])=>st[id]=v);setStock(s,st);const n=Object.keys(SV.edits).length;SV.edits={};svShell();toast(`Estoque salvo (${n}). A vitrine ${STORES[s].code} já está atualizada.`);return}
  const cp=t.closest("[data-svcopy]");if(cp){copy(cp.dataset.svcopy,"Copiado");return}
  if(t.closest("[data-svpos]")){SV.pos={items:[],pag:"pix"};svPos();setTimeout(()=>$("#pos-q")?.focus(),50);return}
  if(t.closest("[data-svposclose]")||t.id==="sv-modal"){closePos();return}
  const pa=t.closest("[data-posadd]");if(pa){readPos();const pr=P.find(x=>x.id==pa.dataset.posadd),st=getStock(TEAM[SV.me].store)[pr.id]??0,it=SV.pos.items.find(x=>x.id===pr.id);if(it){if(it.q<st)it.q++;else toast("Sem mais unidades em estoque")}else SV.pos.items.push({id:pr.id,n:pr.n,p:pr.p,q:1});svPos();return}
  const pr=t.closest("[data-posrem]");if(pr){readPos();SV.pos.items=SV.pos.items.filter(x=>x.id!=pr.dataset.posrem);svPos();return}
  if(t.closest("[data-posok]")){readPos();const m=TEAM[SV.me],st=STORES[m.store],p=SV.pos,sub=p.items.reduce((a,x)=>a+x.p*x.q,0),pixDisc=p.pag==="pix"?sub*.05:0;
    const seq=(+ls.get("sh_seq_"+m.store)||1000)+1;ls.set("sh_seq_"+m.store,String(seq));
    const o={id:`${st.code}-${seq}`,store:m.store,at:new Date().toISOString(),items:p.items,t:{sub,disc:0,pixDisc,fee:0,feeTxt:"Grátis",total:sub-pixDisc},seller:m.name,nome:p.nome.trim()||"Cliente do balcão",whats:p.whats.trim(),tipo:"retirada",slot:"Balcão",pag:p.pag,status:"concluido",origem:"balcao",paid:false,stockOut:true};
    moveStock(o,-1);const os=allOrders();os.unshift(o);saveOrders(os);closePos();SV.tab="pedidos";SV.of="concluidos";SV.open.add(o.id);SV.flash=o.id;svShell();toast(`Venda ${o.id} registrada · comissão de ${brl(o.t.total*commRate())}`);return}
});
document.addEventListener("input",e=>{
  const t=e.target;
  if(t.dataset.pin!=null){t.value=t.value.replace(/\D/g,"").slice(0,1);const i=+t.dataset.pin;if(t.value&&i<3)$(`[data-pin='${i+1}']`).focus();
    const code=[...document.querySelectorAll("[data-pin]")].map(x=>x.value).join("");
    if(code.length===4){if(TEAM[SV.pick].pin===code){SV.me=SV.pick;ls.set("sh_sv_me",SV.me);SV.tab="inicio";svShell();toast(`Bem-vindo(a), ${TEAM[SV.me].name}!`)}else{const pin=$("#pin");pin.classList.remove("bad");void pin.offsetWidth;pin.classList.add("bad");document.querySelectorAll("[data-pin]").forEach(x=>x.value="");$("[data-pin='0']").focus();toast("PIN incorreto")}}return}
  if(t.id==="sv-sq"){SV.sq=t.value;clearTimeout(SV.t);SV.t=setTimeout(()=>{svStock();const i=$("#sv-sq");i.focus();i.setSelectionRange(i.value.length,i.value.length)},200);return}
  if(t.id==="pos-q"){readPos();clearTimeout(SV.t);SV.t=setTimeout(()=>{svPos();const i=$("#pos-q");i.focus();i.setSelectionRange(i.value.length,i.value.length)},150);return}
});
document.addEventListener("change",e=>{
  const t=e.target;
  if(t.id==="sv-sc"){SV.sc=t.value;svStock();return}
  if(t.dataset.svtask){const ts=tasks(),x=ts.find(z=>z.id==t.dataset.svtask);if(x){x.done=t.checked;setTasks(ts);svHome();toast(x.done?"Tarefa concluída":"Tarefa reaberta")}return}
  if(t.dataset.svqi){const id=t.dataset.svqi,st=getStock(TEAM[SV.me].store),v=Math.max(0,parseInt(t.value)||0);if(v===(st[id]??0))delete SV.edits[id];else SV.edits[id]=v;svStock();return}
});
document.addEventListener("keydown",e=>{
  if(e.target.dataset?.pin!=null&&e.key==="Backspace"&&!e.target.value){const i=+e.target.dataset.pin;if(i>0)$(`[data-pin='${i-1}']`).focus()}
  if(e.key==="Escape"&&SV.pos)closePos();
});

/* =========================================================
   PAINEL DOS DONOS (#donos)
   ========================================================= */
const OWNER_PIN="2026";
const OW={auth:false,tab:"geral",store:"all",period:"mes",calM:null,calSel:null,of:{st:"",sel:"",q:""},expF:{},modal:null};
const STORE_COLOR={pnz:"#34925e",lem:"#ffbe00"};
const EV_TYPES={captacao:"Captação de conteúdo",reuniao:"Reunião",fornecedor:"Fornecedor",pagamento:"Pagamento",campanha:"Campanha",folga:"Folga/escala"};
const EXP_CATS=["Aluguel","Energia","Internet","Fornecedor","Marketing","Salários","Impostos","Manutenção","Outros"];

/* ---------- configurações compartilhadas ---------- */
function cfg(){return Object.assign({comm:5,margin:45,goals:{}},lsj.get("sh_cfg",{}))}
function setCfg(c){lsj.set("sh_cfg",c)}
function commRate(){return cfg().comm/100}
function goalOf(k){return cfg().goals[k]??TEAM[k].goal}
function tasks(){return lsj.get("sh_tasks",[])}
function setTasks(t){lsj.set("sh_tasks",t)}

/* ---------- dados de exemplo (marcados) ---------- */
function seedOwner(){
  if(ls.get("sh_seed_owner"))return;
  const d=new Date(),y=d.getFullYear(),m=d.getMonth(),iso=(day,h="09:00")=>`${y}-${String(m+1).padStart(2,"0")}-${String(day).padStart(2,"0")}T${h}`;
  const last=new Date(y,m+1,0).getDate();
  lsj.set("sh_exp",[
    {id:1,desc:"Aluguel da loja",cat:"Aluguel",store:"pnz",val:3500,date:iso(Math.min(10,last)).slice(0,10),paid:false,ex:true},
    {id:2,desc:"Aluguel da loja",cat:"Aluguel",store:"lem",val:3200,date:iso(Math.min(10,last)).slice(0,10),paid:false,ex:true},
    {id:9,desc:"Material de limpeza",cat:"Manutenção",store:"pnz",val:86,date:iso(Math.max(1,new Date().getDate()-2)).slice(0,10),paid:true,ex:true},
    {id:3,desc:"Energia",cat:"Energia",store:"pnz",val:640,date:iso(Math.min(15,last)).slice(0,10),paid:false,ex:true},
    {id:4,desc:"Energia",cat:"Energia",store:"lem",val:580,date:iso(Math.min(15,last)).slice(0,10),paid:false,ex:true},
    {id:5,desc:"Reposição de sedas (distribuidor)",cat:"Fornecedor",store:"pnz",val:2150,date:iso(Math.min(10,last)).slice(0,10),paid:false,ex:true},
    {id:6,desc:"Reposição Tattoo Supply",cat:"Fornecedor",store:"lem",val:1780,date:iso(Math.min(12,last)).slice(0,10),paid:false,ex:true},
    {id:7,desc:"Internet e sistema",cat:"Internet",store:"pnz",val:189,date:iso(Math.min(20,last)).slice(0,10),paid:false,ex:true},
    {id:8,desc:"Tráfego pago (Meta Ads)",cat:"Marketing",store:"pnz",val:1076,date:iso(Math.min(25,last)).slice(0,10),paid:false,ex:true}
  ]);
  const ev=[];let id=1;
  for(let day=1;day<=last;day++){const dw=new Date(y,m,day).getDay();if(dw===1)ev.push({id:id++,title:"Reunião de equipe",type:"reuniao",store:"all",date:iso(day).slice(0,10),time:"08:30",who:"Todos",ex:true})}
  [[Math.min(10,last),"Captação de conteúdo · Conexão","captacao","pnz","10:00","Equipe PNZ"],[Math.min(18,last),"Captação Tattoo Supply · Conexão","captacao","lem","15:00","Bia"],[Math.min(12,last),"Entrega do distribuidor de sedas","fornecedor","pnz","14:00","João"],
   [Math.min(20,last),"Dia da Consciência Negra · card institucional","campanha","all","09:00","Conexão"],[Math.min(27,last),"Black Friday (se aprovada)","campanha","all","08:00","Todos"],[last,"Pagamento de comissões","pagamento","all","17:00","Donos"],
   [Math.min(14,last),"Folga · Carla","folga","pnz","","Carla"]].forEach(([d,t,ty,s,h,w])=>ev.push({id:id++,title:t,type:ty,store:s,date:iso(d).slice(0,10),time:h,who:w,ex:true}));
  lsj.set("sh_events",ev);
  setTasks([
    {id:1,who:"carla",text:"Conferir validade das pomadas Tattoo Supply",done:false,ex:true},
    {id:2,who:"carla",text:"Repor vitrine de isqueiros",done:true,ex:true},
    {id:3,who:"joao",text:"Receber o distribuidor de sedas e conferir a nota",done:false,ex:true},
    {id:4,who:"bia",text:"Fotografar a seleção de vinhos para o site",done:false,ex:true}
  ]);
  ls.set("sh_seed_owner","1");
}

/* ---------- filtros de período e loja ---------- */
function range(p=OW.period){
  const n=new Date(),s=new Date(n);s.setHours(0,0,0,0);
  if(p==="hoje")return[s,n];
  if(p==="7d"){s.setDate(s.getDate()-6);return[s,n]}
  if(p==="30d"){s.setDate(s.getDate()-29);return[s,n]}
  s.setDate(1);return[s,n];
}
function prevRange(){const[a,b]=range(),len=b-a;return[new Date(a-len-1),new Date(a-1)]}
const inR=(iso,[a,b])=>{const t=new Date(iso);return t>=a&&t<=b};
const stOk=o=>OW.store==="all"||o.store===OW.store;
function ordersIn(r=range()){return allOrders().filter(o=>stOk(o)&&inR(o.at,r))}
const sales=os=>os.filter(o=>o.status!=="cancelado");
const sum=(a,f)=>a.reduce((x,o)=>x+f(o),0);
const pct=(a,b)=>b?((a-b)/b*100):null;
const PERIOD_L={hoje:"Hoje","7d":"7 dias",mes:"Este mês","30d":"30 dias"};
function delta(cur,prev){const p=pct(cur,prev);if(p==null)return'<span class="delta">sem base anterior</span>';return `<span class="delta ${p>=0?"up":"dn"}">${p>=0?"▲":"▼"} ${Math.abs(p).toFixed(0)}% vs período anterior</span>`}
const STNAME=k=>k==="all"?"Duas lojas":"Loja "+STORES[k].code;

/* ---------- casca ---------- */
function owLogin(){
  $("#v-owner").innerHTML=`<div class="sv-login"><canvas class="smoke-cv" data-smoke="ow"></canvas><div class="wrap"><div class="card-l">
    <img class="lg" src="${IMG.logo}" alt="Smoke House"><h1>Painel dos <em>donos</em></h1><p>Financeiro, pedidos, equipe e agenda das duas lojas.</p>
    <div class="pin" id="owpin">${[0,1,2,3].map(i=>`<input inputmode="numeric" maxlength="1" type="password" aria-label="Dígito ${i+1} do PIN" data-owpin="${i}">`).join("")}</div>
    <span class="hint">Protótipo: o PIN dos donos é ${OWNER_PIN}.</span>
    <button class="back" data-owexit="1">Voltar para a loja</button></div></div></div>`;
  setTimeout(()=>{if(document.activeElement?.dataset?.owpin==null)$("[data-owpin='0']")?.focus()},60);Smoke.refresh();
}
function owShell(){
  const unpaid=Object.keys(TEAM).reduce((a,k)=>a+sum(allOrders().filter(o=>o.seller===TEAM[k].name&&o.store===TEAM[k].store&&o.status==="concluido"&&!o.paid),o=>o.t.total*commRate()),0);
  const tabs=[["geral","Visão geral"],["fin","Financeiro"],["ped","Pedidos",allOrders().filter(o=>stOk(o)&&o.status==="novo").length],["eq","Equipe"],["ag","Agenda"],["cfg","Ajustes"]];
  $("#v-owner").innerHTML=`<header class="sv-top"><div class="wrap">
      <img src="${IMG.logo}" alt="Smoke House"><span class="tag-s ow-tag">Painel dos donos</span>
      <div class="me"><span class="t"><b>Donos</b><small>${unpaid?`Comissões a pagar: ${brl(unpaid)}`:"Tudo em dia"}</small></span>
      <button class="ghost" data-owstore="1">Ver loja</button><button class="ghost" data-owout="1">Sair</button></div></div>
    <nav class="sv-tabs"><div class="wrap">${tabs.map(([k,l,c])=>`<button data-owtab="${k}" class="${OW.tab===k?"on":""}">${l}${c?`<span class="cnt">${c}</span>`:""}</button>`).join("")}</div></nav></header>
    <main class="wrap sv-main" id="ow-main"></main>`;
  ({geral:owHome,fin:owFin,ped:owOrders,eq:owTeam,ag:owAgenda,cfg:owCfg})[OW.tab]();
}
function owFilters(withPeriod=true){
  return `<div class="ow-bar"><div class="seg" role="group" aria-label="Loja">${[["all","Duas lojas"],["pnz","PNZ"],["lem","LEM"]].map(([k,l])=>`<button data-owst="${k}" class="${OW.store===k?"on":""}">${l}</button>`).join("")}</div>
    ${withPeriod?`<div class="seg" role="group" aria-label="Período">${Object.entries(PERIOD_L).map(([k,l])=>`<button data-owp="${k}" class="${OW.period===k?"on":""}">${l}</button>`).join("")}</div>`:""}
    ${allOrders().some(o=>o.ex)?'<span class="ex-note">Inclui dados de exemplo</span>':""}</div>`;
}

/* ---------- gráficos ---------- */
function lineChart(series,labels){
  const W=640,H=200,pl=48,pr=10,pt=12,pb=24,n=labels.length;
  const mx=Math.max(50,...series.flatMap(s=>s.v)),step=[50,100,200,250,500,1000,2000,2500,5000].find(s=>mx/s<=4)||10000,top=Math.ceil(mx/step)*step;
  const X=i=>pl+(n<2?0:i*(W-pl-pr)/(n-1)),Y=v=>H-pb-(v/top)*(H-pb-pt);
  const grid=[0,.25,.5,.75,1].map(f=>{const v=top*f,y=Y(v);return `<line class="gl" x1="${pl}" x2="${W-pr}" y1="${y}" y2="${y}"/><text x="${pl-6}" y="${y+3}" text-anchor="end">${v>=1000?(v/1000).toLocaleString("pt-BR",{maximumFractionDigits:1})+" mil":Math.round(v)}</text>`}).join("");
  const every=Math.ceil(n/8);
  const xl=labels.map((l,i)=>i%every===0||i===n-1?`<text x="${X(i)}" y="${H-6}" text-anchor="middle">${l}</text>`:"").join("");
  const paths=series.map(s=>{const pts=s.v.map((v,i)=>`${X(i)},${Y(v)}`).join(" ");return `<polygon class="ar" fill="${s.c}" points="${X(0)},${Y(0)} ${pts} ${X(n-1)},${Y(0)}"/><polyline class="ln" stroke="${s.c}" points="${pts}"/>${s.v.map((v,i)=>`<circle class="dot" fill="${s.c}" cx="${X(i)}" cy="${Y(v)}" r="${n>20?2.5:3.5}"><title>${s.name} · ${labels[i]}: ${brl(v)}</title></circle>`).join("")}`}).join("");
  return `<svg class="lc" viewBox="0 0 ${W} ${H}" role="img" aria-label="Faturamento por dia">${grid}${xl}${paths}</svg>`;
}
function donut(parts,center,sub){
  const tot=parts.reduce((a,p)=>a+p.v,0)||1,r=56,C=2*Math.PI*r;let off=0;
  const segs=parts.map(p=>{const len=p.v/tot*C,s=`<circle r="${r}" cx="75" cy="75" stroke="${p.c}" stroke-dasharray="${len} ${C-len}" stroke-dashoffset="${-off}" transform="rotate(-90 75 75)"><title>${p.l}: ${brl(p.v)}</title></circle>`;off+=len;return s}).join("");
  return `<div class="donut-wrap"><svg class="donut" viewBox="0 0 150 150" width="150" height="150"><circle r="${r}" cx="75" cy="75" stroke="var(--bg)"/>${segs}<text class="c" x="75" y="78" text-anchor="middle">${center}</text><text class="s" x="75" y="94" text-anchor="middle">${sub}</text></svg>
    <div class="dl">${parts.map(p=>`<div><i style="background:${p.c}"></i><span>${p.l}</span><b>${brl(p.v)}</b><small>${Math.round(p.v/tot*100)}%</small></div>`).join("")}</div></div>`;
}
function dailySeries(r){
  const days=[];const d=new Date(r[0]);d.setHours(0,0,0,0);while(d<=r[1]){days.push(new Date(d));d.setDate(d.getDate()+1)}
  const keys=OW.store==="all"?["pnz","lem"]:[OW.store];
  const os=sales(allOrders().filter(o=>inR(o.at,r)));
  return{labels:days.map(x=>`${x.getDate()}/${x.getMonth()+1}`),series:keys.map(k=>({name:"Loja "+STORES[k].code,c:STORE_COLOR[k],v:days.map(x=>sum(os.filter(o=>o.store===k&&new Date(o.at).toDateString()===x.toDateString()),o=>o.t.total))}))};
}

/* ---------- visão geral ---------- */
function owHome(){
  const r=range(),cur=sales(ordersIn(r)),prev=sales(ordersIn(prevRange()));
  const fat=sum(cur,o=>o.t.total),fatP=sum(prev,o=>o.t.total),tk=cur.length?fat/cur.length:0,tkP=prev.length?fatP/prev.length:0;
  const unpaid=sum(allOrders().filter(o=>stOk(o)&&o.status==="concluido"&&!o.paid&&o.seller),o=>o.t.total*commRate());
  const active=allOrders().filter(o=>stOk(o)&&ACTIVE.includes(o.status));
  const rr=OW.period==="hoje"?range("7d"):r,ds=dailySeries(rr);
  const prodMap={};cur.forEach(o=>o.items.forEach(x=>{prodMap[x.n]=(prodMap[x.n]||0)+x.p*x.q}));
  const top=Object.entries(prodMap).sort((a,b)=>b[1]-a[1]).slice(0,6),tmax=top[0]?.[1]||1;
  const site=sum(cur.filter(o=>o.origem!=="balcao"),o=>o.t.total),balc=sum(cur.filter(o=>o.origem==="balcao"),o=>o.t.total);
  const pays=PAYMENTS.map(p=>({l:p.short,c:p.c,v:sum(cur.filter(o=>PAYK(o.pag)===p.k),o=>o.t.total)})).filter(x=>x.v>0);
  const low=(OW.store==="all"?["pnz","lem"]:[OW.store]).flatMap(s=>{const st=getStock(s);return P.filter(p=>(st[p.id]??0)<MIN_STOCK).map(p=>({p,s,q:st[p.id]??0}))}).sort((a,b)=>a.q-b.q);
  const today=new Date().toISOString().slice(0,10),evs=lsj.get("sh_events",[]).filter(e=>e.date>=today&&(OW.store==="all"||e.store==="all"||e.store===OW.store)).sort((a,b)=>(a.date+a.time).localeCompare(b.date+b.time)).slice(0,5);
  const byStore=["pnz","lem"].map(k=>({k,v:sum(sales(allOrders().filter(o=>o.store===k&&inR(o.at,r))),o=>o.t.total),n:sales(allOrders().filter(o=>o.store===k&&inR(o.at,r))).length}));
  $("#ow-main").innerHTML=`<div class="sv-h"><div><h2>Visão <em>geral</em></h2><p>${STNAME(OW.store)} · ${PERIOD_L[OW.period].toLowerCase()}</p></div></div>${owFilters()}
    <div class="kpis k5">
      <div class="kpi dark"><span>Faturamento</span><b>${brl(fat)}</b>${delta(fat,fatP)}</div>
      <div class="kpi"><span>Pedidos</span><b>${cur.length}</b>${delta(cur.length,prev.length)}</div>
      <div class="kpi"><span>Ticket médio</span><b>${brl(tk)}</b>${delta(tk,tkP)}</div>
      <div class="kpi"><span>Em andamento agora</span><b>${active.length}</b><small>${active.filter(o=>o.status==="novo").length} novos sem confirmação</small></div>
      <div class="kpi"><span>Comissões a pagar</span><b>${brl(unpaid)}</b><small>${cfg().comm}% sobre concluídos</small></div>
    </div>
    <div class="sv-grid">
      <div style="display:grid;gap:16px">
        <div class="panel"><h3>Faturamento por dia${OW.period==="hoje"?" · últimos 7 dias":""}<span class="legend">${ds.series.map(s=>`<span><i style="background:${s.c}"></i>${s.name}</span>`).join("")}</span></h3>${lineChart(ds.series,ds.labels)}</div>
        ${OW.store==="all"?`<div class="panel"><h3>Comparativo das lojas</h3><div class="cmp">${byStore.map(b=>`<div><span>Loja ${STORES[b.k].code}</span><b style="color:${b.k==="pnz"?"var(--green)":"#a87700"}">${brl(b.v)}</b><small>${b.n} pedidos · ticket ${brl(b.n?b.v/b.n:0)}</small></div>`).join("")}</div></div>`:""}
        <div class="panel"><h3>Mais vendidos no período</h3><div class="hbars">${top.length?top.map(([n,v])=>`<div><div class="t"><span>${esc(n)}</span><b>${brl(v)}</b></div><div class="b"><i style="width:${v/tmax*100}%"></i></div></div>`).join(""):'<p class="note">Sem vendas no período.</p>'}</div></div>
      </div>
      <div style="display:grid;gap:16px">
        <div class="panel"><h3>Formas de pagamento</h3>${donut(pays,cur.length,"pedidos")}</div>
        <div class="panel"><h3>Canal de venda</h3>${donut([{l:"Site e link",c:"#34925e",v:site},{l:"Balcão",c:"#0e0f0d",v:balc}],fat>=1000?(fat/1000).toLocaleString("pt-BR",{maximumFractionDigits:1})+" mil":Math.round(fat),"R$ no período")}</div>
        <div class="panel"><h3>Próximos compromissos <button data-owtab="ag">Abrir agenda</button></h3><div class="ev-list">${evs.length?evs.map(e=>evItem(e,false)).join(""):'<p class="note">Nada agendado.</p>'}</div></div>
        <div class="panel"><h3>Estoque baixo <span style="font-weight:500;font-size:12px;color:var(--muted)">${low.length} itens</span></h3><div class="mini-list">${low.slice(0,6).map(x=>`<div class="mini-row"><span><b>${esc(x.p.n)}</b><small>Loja ${STORES[x.s].code}</small></span><span class="pill ${x.q?"warnp":"lowp"}">${x.q?x.q+" un.":"Esgotado"}</span></div>`).join("")||'<p class="note">Tudo abastecido.</p>'}</div></div>
      </div>
    </div>`;
}

/* ---------- financeiro ---------- */
function owFin(){
  const r=range(),os=sales(ordersIn(r)),done=os.filter(o=>o.status==="concluido");
  const gross=sum(os,o=>o.t.sub),disc=sum(os,o=>(o.t.disc||0)+(o.t.pixDisc||0)),fees=sum(os,o=>o.t.fee||0);
  const net=gross-disc,cmv=net*(1-cfg().margin/100),gp=net-cmv,comm=sum(os.filter(o=>o.seller),o=>o.t.total*commRate());
  const exps=lsj.get("sh_exp",[]).filter(e=>(OW.store==="all"||e.store===OW.store)&&inR(e.date+"T12:00",r));
  const expT=sum(exps,e=>e.val),result=gp+fees-comm-expT;
  const cashIn=sum(done,o=>o.t.total),cashOut=sum(exps.filter(e=>e.paid),e=>e.val)+sum(allOrders().filter(o=>stOk(o)&&o.paid&&o.paidAt&&inR(o.paidAt,r)),o=>o.t.total*commRate());
  const toPay=lsj.get("sh_exp",[]).filter(e=>!e.paid&&(OW.store==="all"||e.store===OW.store)).sort((a,b)=>a.date.localeCompare(b.date));
  const byCat={};exps.forEach(e=>byCat[e.cat]=(byCat[e.cat]||0)+e.val);const cmax=Math.max(1,...Object.values(byCat));
  const f=OW.expF;
  $("#ow-main").innerHTML=`<div class="sv-h"><div><h2>Financeiro</h2><p>${STNAME(OW.store)} · ${PERIOD_L[OW.period].toLowerCase()}</p></div></div>${owFilters()}
    <div class="kpis">
      <div class="kpi dark"><span>Resultado estimado</span><b class="${result>=0?"":"neg"}" style="${result>=0?"":"color:#ff8a8c"}">${brl(result)}</b><small>depois de custos, comissões e despesas</small></div>
      <div class="kpi"><span>Entradas (concluídos)</span><b>${brl(cashIn)}</b><small>${done.length} pedidos recebidos</small></div>
      <div class="kpi"><span>Saídas pagas</span><b>${brl(cashOut)}</b><small>despesas e comissões pagas</small></div>
      <div class="kpi"><span>Saldo de caixa</span><b class="${cashIn-cashOut>=0?"pos":"neg"}">${brl(cashIn-cashOut)}</b><small>entradas menos saídas</small></div>
    </div>
    <div class="sv-grid">
      <div style="display:grid;gap:16px">
        <div class="panel"><h3>Demonstrativo do período</h3><table class="dre"><tbody>
          <tr><td>Vendas brutas <small>(${os.length} pedidos)</small></td><td>${brl(gross)}</td></tr>
          <tr class="neg"><td>(−) Descontos <small>3 por 2 e Pix</small></td><td>−${brl(disc)}</td></tr>
          <tr class="sub"><td>Receita líquida de produtos</td><td>${brl(net)}</td></tr>
          <tr class="neg"><td>(−) Custo dos produtos <small>estimado com margem de ${cfg().margin}%</small></td><td>−${brl(cmv)}</td></tr>
          <tr class="sub"><td>Lucro bruto</td><td>${brl(gp)}</td></tr>
          <tr><td>(+) Taxas de entrega</td><td>${brl(fees)}</td></tr>
          <tr class="neg"><td>(−) Comissões da equipe <small>${cfg().comm}%</small></td><td>−${brl(comm)}</td></tr>
          <tr class="neg"><td>(−) Despesas <small>${exps.length} ${exps.length===1?"lançamento":"lançamentos"}</small></td><td>−${brl(expT)}</td></tr>
          <tr class="res"><td>Resultado</td><td class="${result>=0?"pos":"neg"}">${brl(result)}</td></tr>
        </tbody></table><p class="note">O custo dos produtos é estimado pela margem definida em Ajustes. Com o custo real de cada item cadastrado, o cálculo fica exato.</p></div>
        <div class="panel"><h3>Lançar despesa</h3>
          <div class="exp-form">
            <div class="fld"><label for="ex-desc">Descrição</label><input id="ex-desc" value="${esc(f.desc||"")}" placeholder="Ex.: conta de energia"></div>
            <div class="fld"><label for="ex-cat">Categoria</label><select id="ex-cat">${EXP_CATS.map(c=>`<option ${f.cat===c?"selected":""}>${c}</option>`).join("")}</select></div>
            <div class="fld"><label for="ex-store">Loja</label><select id="ex-store"><option value="pnz" ${f.store==="pnz"?"selected":""}>PNZ</option><option value="lem" ${f.store==="lem"?"selected":""}>LEM</option></select></div>
            <div class="fld"><label for="ex-val">Valor (R$)</label><input id="ex-val" inputmode="decimal" value="${esc(f.val||"")}" placeholder="0,00"></div>
            <div class="fld"><label for="ex-date">Vencimento</label><input id="ex-date" type="date" value="${f.date||new Date().toISOString().slice(0,10)}"></div>
            <button class="btn btn-green" data-owexpadd="1">Lançar</button>
          </div><p class="note" id="ex-msg"></p></div>
      </div>
      <div style="display:grid;gap:16px">
        <div class="panel"><h3>Contas a pagar <span style="font-weight:500;font-size:12px;color:var(--muted)">${brl(sum(toPay,e=>e.val))}</span></h3><div class="mini-list">${toPay.length?toPay.map(e=>{const late=e.date<new Date().toISOString().slice(0,10);return `<div class="mini-row"><span><b>${esc(e.desc)}</b><small>${e.cat} · Loja ${STORES[e.store].code} · vence ${new Date(e.date+"T12:00").toLocaleDateString("pt-BR")}${late?' · <b style="color:var(--hot)">atrasada</b>':""}${e.ex?" · exemplo":""}</small></span><span style="display:flex;gap:8px;align-items:center"><b>${brl(e.val)}</b><button class="btn btn-dark btn-sm" data-owpay="${e.id}">Pagar</button></span></div>`}).join(""):'<p class="note">Nenhuma conta em aberto.</p>'}</div></div>
        <div class="panel"><h3>Despesas por categoria</h3><div class="hbars">${Object.entries(byCat).sort((a,b)=>b[1]-a[1]).map(([c,v])=>`<div><div class="t"><span>${c}</span><b>${brl(v)}</b></div><div class="b"><i style="width:${v/cmax*100}%;background:var(--ink)"></i></div></div>`).join("")||'<p class="note">Sem despesas no período.</p>'}</div></div>
        <div class="panel"><h3>Recebimentos por forma</h3>${donut(PAYMENTS.map(p=>({l:p.short,c:p.c,v:sum(done.filter(o=>PAYK(o.pag)===p.k),o=>o.t.total)})).filter(x=>x.v>0),done.length,"concluídos")}</div>
      </div>
    </div>`;
}

/* ---------- pedidos ---------- */
function owOrders(){
  const f=OW.of,q=norm(f.q||"");
  let os=allOrders().filter(o=>stOk(o)&&inR(o.at,range()));
  if(f.st)os=os.filter(o=>f.st==="ativos"?ACTIVE.includes(o.status):o.status===f.st);
  if(f.sel)os=os.filter(o=>f.sel==="-"?!o.seller:o.seller===f.sel);
  if(q)os=os.filter(o=>norm(o.id+" "+o.nome+" "+(o.seller||"")+" "+o.items.map(x=>x.n).join(" ")).includes(q));
  const sellers=[...new Set(allOrders().filter(stOk).map(o=>o.seller).filter(Boolean))];
  $("#ow-main").innerHTML=`<div class="sv-h"><div><h2>Pedidos</h2><p>${os.length} pedidos · ${brl(sum(sales(os),o=>o.t.total))} em vendas</p></div></div>${owFilters()}
    <div class="stock-tools"><input id="ow-oq" type="search" placeholder="Buscar por número, cliente, produto ou colaborador" value="${esc(f.q||"")}" aria-label="Buscar pedidos">
      <select id="ow-ost" aria-label="Status"><option value="">Todos os status</option><option value="ativos" ${f.st==="ativos"?"selected":""}>Em andamento</option>${Object.entries(STL).map(([k,l])=>`<option value="${k}" ${f.st===k?"selected":""}>${l}</option>`).join("")}</select>
      <select id="ow-osel" aria-label="Colaborador"><option value="">Todos os colaboradores</option>${sellers.map(s=>`<option ${f.sel===s?"selected":""}>${esc(s)}</option>`).join("")}<option value="-" ${f.sel==="-"?"selected":""}>Sem atendente</option></select></div>
    <div class="tbl-wrap"><table class="ext ow-orders" style="min-width:760px"><thead><tr><th>Pedido</th><th>Data</th><th>Loja</th><th>Cliente</th><th>Colaborador</th><th>Canal</th><th class="num">Total</th><th>Status</th></tr></thead><tbody>
      ${os.map(o=>`<tr data-owo="${o.id}"><td><b>${o.id}</b>${o.ex?' <small style="color:var(--muted)">ex.</small>':""}</td><td>${fmtWhen(o.at)}</td><td>${STORES[o.store].code}</td><td>${esc(o.nome)}</td><td>${o.seller?esc(o.seller):'<span style="color:var(--hot)">Sem atendente</span>'}</td><td>${o.origem==="balcao"?"Balcão":"Site"}</td><td class="num"><b>${brl(o.t.total)}</b></td><td>${pill(o.status)}</td></tr>`).join("")||'<tr><td colspan="8" style="text-align:center;color:var(--muted);padding:28px">Nenhum pedido com esses filtros.</td></tr>'}
    </tbody></table></div>`;
}
function owOrderModal(id){
  const o=allOrders().find(x=>x.id===id);if(!o)return;
  const sellers=Object.entries(TEAM).filter(([k,t])=>t.store===o.store);
  owModal(`<h3>${o.id}<button data-owclose="1" aria-label="Fechar">×</button></h3>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">${pill(o.status)}<span class="note">${fmtWhen(o.at)} · Loja ${STORES[o.store].code} · ${o.origem==="balcao"?"Balcão":"Site"}</span></div>
    <div class="o-items">${o.items.map(x=>`<div><span>${x.q}× ${esc(x.n)}</span><span>${brl(x.p*x.q)}</span></div>`).join("")}${o.t.disc?`<div style="color:var(--green)"><span>Promoção 3 por 2</span><span>-${brl(o.t.disc)}</span></div>`:""}${o.t.pixDisc?`<div style="color:var(--green)"><span>Desconto Pix</span><span>-${brl(o.t.pixDisc)}</span></div>`:""}${o.t.fee?`<div><span>Entrega</span><span>${brl(o.t.fee)}</span></div>`:""}<div style="font-weight:800"><span>Total</span><span>${brl(o.t.total)}</span></div></div>
    <div class="o-meta"><div><span>Cliente</span>${esc(o.nome)}<br>${esc(o.whats||"—")}</div><div><span>${o.tipo==="entrega"?"Entrega":"Retirada"}</span>${o.tipo==="entrega"?`${esc(o.rua||"")}, ${esc(o.num||"")} · ${esc(o.bairro||"")}`:esc(o.slot||"Na loja")}</div><div><span>Pagamento</span>${esc(payLabel(o,true))}</div><div><span>Comissão</span>${o.seller&&o.status!=="cancelado"?brl(o.t.total*commRate())+(o.paid?" · paga":o.status==="concluido"?" · a pagar":" · prevista"):"—"}</div></div>
    <div class="fld"><label for="ow-reassign">Colaborador responsável</label><select id="ow-reassign" data-owreassign="${o.id}"><option value="">Sem atendente</option>${sellers.map(([k,t])=>`<option value="${esc(t.name)}" ${o.seller===t.name?"selected":""}>${esc(t.name)}</option>`).join("")}</select></div>
    ${o.whats?`<a class="btn btn-dark" target="_blank" rel="noopener" href="${waLink(o.whats,`Olá, ${o.nome.split(" ")[0]}! Aqui é da Smoke House ${STORES[o.store].code}, sobre o pedido ${o.id}.`)}">Falar com o cliente</a>`:""}`);
}

/* ---------- equipe ---------- */
function owTeam(){
  const r=range(),c=cfg();
  const list=Object.entries(TEAM).filter(([k,t])=>OW.store==="all"||t.store===OW.store).map(([k,t])=>{
    const mine=allOrders().filter(o=>o.seller===t.name&&o.store===t.store),per=sales(mine.filter(o=>inR(o.at,r))),month=sales(mine.filter(o=>inR(o.at,range("mes"))));
    return{k,t,v:sum(per,o=>o.t.total),n:per.length,mv:sum(month,o=>o.t.total),unpaid:mine.filter(o=>o.status==="concluido"&&!o.paid),paid:sum(mine.filter(o=>o.paid),o=>o.t.total*commRate())};
  }).sort((a,b)=>b.v-a.v);
  const tk=tasks();
  $("#ow-main").innerHTML=`<div class="sv-h"><div><h2>Equipe</h2><p>Desempenho, meta, comissão e tarefas de cada colaborador. As tarefas aparecem na área de cada um.</p></div><button class="btn btn-green btn-sm" data-ownew="1">+ Novo colaborador</button></div>${owFilters()}
    <div class="team">${list.map((x,i)=>{const g=goalOf(x.k),p=Math.min(100,x.mv/g*100),due=sum(x.unpaid,o=>o.t.total*commRate()),my=tk.filter(t=>t.who===x.k);return `<article class="tm">
      <div class="tm-h">${avatar(x.k)}<div><b>${esc(x.t.name)}</b><small>Loja ${STORES[x.t.store].code} · PIN ${x.t.pin}</small></div><span class="rk">${i+1}º</span></div>
      <div class="tm-k"><div><span>Vendas</span><b>${brl(x.v)}</b></div><div><span>Pedidos</span><b>${x.n}</b></div><div><span>Ticket</span><b>${brl(x.n?x.v/x.n:0)}</b></div></div>
      <div><div class="goal-txt" style="margin-bottom:6px"><span>Meta do mês · <b>${Math.round(p)}%</b></span><span>${brl(x.mv)} de ${brl(g)}</span></div><div class="goal-bar"><i style="width:${p}%;transition:none"></i></div></div>
      <div class="inline"><label for="goal-${x.k}">Meta mensal (R$)</label><input id="goal-${x.k}" data-owgoal="${x.k}" inputmode="numeric" value="${g}"></div>
      <div class="mini-row" style="cursor:default"><span><b>Comissão a pagar: ${brl(due)}</b><small>${x.unpaid.length} pedidos concluídos · já pago ${brl(x.paid)}</small></span>${due?`<button class="btn btn-yellow btn-sm" data-owpaycomm="${x.k}">Pagar</button>`:'<span class="pill okp">Em dia</span>'}</div>
      <div><b style="font-size:13px">Tarefas</b><div class="tasks" style="margin-top:6px">${my.map(t=>`<label class="task ${t.done?"dn":""}"><input type="checkbox" data-owtask="${t.id}" ${t.done?"checked":""}><span>${esc(t.text)}</span>${t.ex?"<small>ex.</small>":""}<button data-owtaskdel="${t.id}" aria-label="Excluir tarefa">×</button></label>`).join("")||'<p class="note">Sem tarefas.</p>'}</div>
      <div class="add-task" style="margin-top:6px"><input id="nt-${x.k}" placeholder="Nova tarefa para ${esc(x.t.name)}" aria-label="Nova tarefa"><button class="btn btn-dark btn-sm" data-owtaskadd="${x.k}">Adicionar</button></div></div>
    </article>`}).join("")}</div>`;
}

/* ---------- agenda ---------- */
function evItem(e,del=true){return `<div class="ev-item"><span class="h">${e.time||"Dia todo"}</span><span><b>${esc(e.title)}</b><small><span class="pill ev-t-${e.type}" style="padding:2px 8px;font-size:10.5px">${EV_TYPES[e.type]}</span> ${new Date(e.date+"T12:00").toLocaleDateString("pt-BR",{weekday:"short",day:"2-digit",month:"2-digit"})} · ${e.store==="all"?"Duas lojas":"Loja "+STORES[e.store].code}${e.who?" · "+esc(e.who):""}${e.ex?" · exemplo":""}</small></span>${del?`<button data-owevdel="${e.id}" aria-label="Excluir compromisso">×</button>`:"<span></span>"}</div>`}
function owAgenda(){
  const now=new Date();if(!OW.calM)OW.calM=new Date(now.getFullYear(),now.getMonth(),1);if(!OW.calSel)OW.calSel=now.toISOString().slice(0,10);
  const m=OW.calM,y=m.getFullYear(),mo=m.getMonth(),first=new Date(y,mo,1),start=new Date(first);start.setDate(1-first.getDay());
  const evs=lsj.get("sh_events",[]).filter(e=>OW.store==="all"||e.store==="all"||e.store===OW.store);
  const today=now.toISOString().slice(0,10),cells=[];
  for(let i=0;i<42;i++){const d=new Date(start);d.setDate(start.getDate()+i);const k=`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;cells.push({d,k,e:evs.filter(e=>e.date===k).sort((a,b)=>(a.time||"").localeCompare(b.time||""))})}
  const rows=cells[35].d.getMonth()!==mo?35:42;
  const sel=evs.filter(e=>e.date===OW.calSel).sort((a,b)=>(a.time||"").localeCompare(b.time||""));
  $("#ow-main").innerHTML=`<div class="sv-h"><div><h2>Agenda</h2><p>Captações, fornecedores, reuniões, pagamentos e escala das lojas.</p></div></div>${owFilters(false)}
    <div class="sv-grid">
      <div class="panel"><div class="cal-head"><b>${m.toLocaleDateString("pt-BR",{month:"long",year:"numeric"})}</b><div class="row"><button class="btn btn-line btn-sm" style="color:var(--fg);border-color:var(--line)" data-owcal="-1" aria-label="Mês anterior">‹</button><button class="btn btn-line btn-sm" style="color:var(--fg);border-color:var(--line)" data-owcal="0">Hoje</button><button class="btn btn-line btn-sm" style="color:var(--fg);border-color:var(--line)" data-owcal="1" aria-label="Próximo mês">›</button></div></div>
        <div class="cal">${["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"].map(d=>`<span class="dow">${d}</span>`).join("")}
        ${cells.slice(0,rows).map(c=>`<button class="d ${c.d.getMonth()!==mo?"out":""} ${c.k===today?"today":""} ${c.k===OW.calSel?"sel":""}" data-owday="${c.k}" aria-label="${c.d.toLocaleDateString("pt-BR")}, ${c.e.length} compromissos"><span class="n">${c.d.getDate()}</span>${c.e.slice(0,2).map(e=>`<span class="ev ev-t-${e.type}">${e.time?e.time+" ":""}${esc(e.title)}</span>`).join("")}${c.e.length>2?`<span class="more">+${c.e.length-2} mais</span>`:""}</button>`).join("")}</div>
        <div class="legend" style="margin-top:10px">${Object.entries(EV_TYPES).map(([k,l])=>`<span><i class="ev-t-${k}" style="height:10px;width:10px;border-radius:3px"></i>${l}</span>`).join("")}</div></div>
      <div style="display:grid;gap:16px">
        <div class="panel"><h3>${new Date(OW.calSel+"T12:00").toLocaleDateString("pt-BR",{weekday:"long",day:"numeric",month:"long"})}</h3><div class="ev-list">${sel.length?sel.map(e=>evItem(e)).join(""):'<p class="note">Nenhum compromisso neste dia.</p>'}</div></div>
        <div class="panel"><h3>Novo compromisso</h3>
          <div class="fields">
            <div class="fld full"><label for="ev-title">Título</label><input id="ev-title" placeholder="Ex.: captação de Reels"></div>
            <div class="fld"><label for="ev-date">Data</label><input id="ev-date" type="date" value="${OW.calSel}"></div>
            <div class="fld"><label for="ev-time">Horário</label><input id="ev-time" type="time"></div>
            <div class="fld"><label for="ev-type">Tipo</label><select id="ev-type">${Object.entries(EV_TYPES).map(([k,l])=>`<option value="${k}">${l}</option>`).join("")}</select></div>
            <div class="fld"><label for="ev-store">Loja</label><select id="ev-store"><option value="all">Duas lojas</option><option value="pnz" ${OW.store==="pnz"?"selected":""}>PNZ</option><option value="lem" ${OW.store==="lem"?"selected":""}>LEM</option></select></div>
            <div class="fld full"><label for="ev-who">Responsável</label><input id="ev-who" placeholder="Opcional"></div>
          </div><p class="note" id="ev-msg"></p>
          <button class="btn btn-green" data-owevadd="1" style="justify-self:start">Agendar</button></div>
      </div>
    </div>`;
}

/* ---------- ajustes ---------- */
function owCfg(){
  const c=cfg();
  $("#ow-main").innerHTML=`<div class="sv-h"><div><h2>Ajustes</h2><p>Regras que valem para o painel, para a área do colaborador e para a vitrine.</p></div></div>
    <div class="sv-grid"><div class="panel"><h3>Comissão e custos</h3><div class="cfg">
      <label for="cfg-comm">Comissão dos colaboradores (%)<input id="cfg-comm" inputmode="decimal" value="${c.comm}"></label>
      <label for="cfg-margin">Margem bruta média estimada (%)<input id="cfg-margin" inputmode="decimal" value="${c.margin}"></label>
      <label for="cfg-min">Estoque mínimo para alerta (un.)<input id="cfg-min" value="${MIN_STOCK}" disabled></label>
    </div><button class="btn btn-green" data-owcfgsave="1" style="justify-self:start">Salvar ajustes</button></div>
    <div class="panel"><h3>Dados do protótipo</h3><div class="note-box">Neste protótipo, pedidos, estoque, despesas e agenda ficam salvos no navegador. No sistema final, tudo fica num banco de dados compartilhado entre donos e colaboradores, com acesso por login individual.</div>
      <button class="btn btn-line btn-sm" style="color:var(--hot);justify-self:start" data-owreset="1">Restaurar dados de exemplo</button></div></div>`;
}

/* ---------- modal genérico ---------- */
function owModal(html){let md=$("#ow-modal");if(!md){md=document.createElement("div");md.id="ow-modal";md.className="modal";document.body.appendChild(md)}md.innerHTML=`<div class="modal-box" role="dialog">${html}</div>`}
function owCloseModal(){$("#ow-modal")?.remove()}

function renderOW(){seedOrders();seedOwner();OW.auth=ls.get("sh_ow")==="1";OW.auth?owShell():owLogin()}

document.addEventListener("click",e=>{
  if($("#v-owner").hidden&&!e.target.closest("#ow-modal")&&!e.target.closest("[data-ow]"))return;
  const t=e.target;
  if(t.closest("[data-ow]")){location.hash="donos";return}
  if(t.closest("[data-owexit]")){location.hash=ls.get("sh_age")==="ok"?"pnz":"";return}
  if(t.closest("[data-owout]")){OW.auth=false;try{localStorage.removeItem("sh_ow")}catch(_){}owLogin();return}
  if(t.closest("[data-owstore]")){ls.set("sh_age","ok");location.hash=OW.store==="lem"?"lem":"pnz";return}
  const tab=t.closest("[data-owtab]");if(tab){OW.tab=tab.dataset.owtab;owShell();window.scrollTo(0,0);return}
  const st=t.closest("[data-owst]");if(st){OW.store=st.dataset.owst;owShell();return}
  const pp=t.closest("[data-owp]");if(pp){OW.period=pp.dataset.owp;owShell();return}
  const oo=t.closest("[data-owo]");if(oo){owOrderModal(oo.dataset.owo);return}
  if(t.closest("[data-owclose]")||t.id==="ow-modal"){owCloseModal();return}
  if(t.closest("[data-owexpadd]")){
    const desc=$("#ex-desc").value.trim(),val=parseFloat($("#ex-val").value.replace(/\./g,"").replace(",","."));
    OW.expF={desc,cat:$("#ex-cat").value,store:$("#ex-store").value,val:$("#ex-val").value,date:$("#ex-date").value};
    if(!desc||!(val>0)||!OW.expF.date){$("#ex-msg").textContent="Preencha descrição, valor e vencimento.";$("#ex-msg").style.color="var(--hot)";return}
    const ex=lsj.get("sh_exp",[]);ex.push({id:Date.now(),desc,cat:OW.expF.cat,store:OW.expF.store,val,date:OW.expF.date,paid:false});lsj.set("sh_exp",ex);OW.expF={};owFin();toast("Despesa lançada em contas a pagar");return}
  const pay=t.closest("[data-owpay]");if(pay){const ex=lsj.get("sh_exp",[]),x=ex.find(z=>z.id==pay.dataset.owpay);if(x){x.paid=true;lsj.set("sh_exp",ex);owFin();toast(`${x.desc} marcada como paga`)}return}
  const pc=t.closest("[data-owpaycomm]");if(pc){const k=pc.dataset.owpaycomm,tm=TEAM[k];if(pc.dataset.sure!=="1"){pc.dataset.sure="1";pc.textContent="Confirmar pagamento";return}
    const os=allOrders();let v=0;os.forEach(o=>{if(o.seller===tm.name&&o.store===tm.store&&o.status==="concluido"&&!o.paid){o.paid=true;o.paidAt=new Date().toISOString();v+=o.t.total*commRate()}});saveOrders(os);owShell();toast(`Comissão de ${brl(v)} paga para ${tm.name}`);return}
  const tk=t.closest("[data-owtaskadd]");if(tk){const k=tk.dataset.owtaskadd,i=$("#nt-"+k),txt=i.value.trim();if(!txt){i.focus();return}const ts=tasks();ts.push({id:Date.now(),who:k,text:txt,done:false});setTasks(ts);owTeam();toast(`Tarefa enviada para ${TEAM[k].name}`);return}
  const td=t.closest("[data-owtaskdel]");if(td){e.preventDefault();setTasks(tasks().filter(x=>x.id!=td.dataset.owtaskdel));owTeam();return}
  if(t.closest("[data-ownew]")){owModal(`<h3>Novo colaborador<button data-owclose="1" aria-label="Fechar">×</button></h3>
    <div class="fields"><div class="fld full"><label for="nc-name">Nome</label><input id="nc-name" placeholder="Primeiro nome"></div><div class="fld"><label for="nc-store">Loja</label><select id="nc-store"><option value="pnz">PNZ</option><option value="lem">LEM</option></select></div><div class="fld"><label for="nc-pin">PIN (4 dígitos)</label><input id="nc-pin" inputmode="numeric" maxlength="4" placeholder="0000"></div><div class="fld full"><label for="nc-goal">Meta mensal (R$)</label><input id="nc-goal" inputmode="numeric" value="2500"></div></div>
    <p class="note" id="nc-msg">O link de venda é criado automaticamente.</p><button class="btn btn-green" data-owncsave="1">Cadastrar</button>`);setTimeout(()=>$("#nc-name")?.focus(),50);return}
  if(t.closest("[data-owncsave]")){const name=$("#nc-name").value.trim(),pin=$("#nc-pin").value.trim(),store=$("#nc-store").value,goal=parseInt($("#nc-goal").value)||2500;
    const key=norm(name).replace(/[^a-z]/g,"");
    if(!name||!/^\d{4}$/.test(pin)){$("#nc-msg").textContent="Digite o nome e um PIN de 4 números.";$("#nc-msg").style.color="var(--hot)";return}
    if(TEAM[key]||SELLERS[key]){$("#nc-msg").textContent="Já existe um colaborador com esse nome.";$("#nc-msg").style.color="var(--hot)";return}
    const extra=lsj.get("sh_team",{});extra[key]={name,store,pin,goal,cls:""};lsj.set("sh_team",extra);loadTeam();owCloseModal();OW.tab="eq";owShell();toast(`${name} cadastrado(a) na loja ${STORES[store].code}`);return}
  const cal=t.closest("[data-owcal]");if(cal){const d=+cal.dataset.owcal;if(!d){const n=new Date();OW.calM=new Date(n.getFullYear(),n.getMonth(),1);OW.calSel=n.toISOString().slice(0,10)}else OW.calM=new Date(OW.calM.getFullYear(),OW.calM.getMonth()+d,1);owAgenda();return}
  const day=t.closest("[data-owday]");if(day){OW.calSel=day.dataset.owday;const d=new Date(OW.calSel+"T12:00");if(d.getMonth()!==OW.calM.getMonth())OW.calM=new Date(d.getFullYear(),d.getMonth(),1);owAgenda();return}
  if(t.closest("[data-owevadd]")){const title=$("#ev-title").value.trim(),date=$("#ev-date").value;if(!title||!date){$("#ev-msg").textContent="Digite o título e a data.";$("#ev-msg").style.color="var(--hot)";return}
    const ev=lsj.get("sh_events",[]);ev.push({id:Date.now(),title,date,time:$("#ev-time").value,type:$("#ev-type").value,store:$("#ev-store").value,who:$("#ev-who").value.trim()});lsj.set("sh_events",ev);OW.calSel=date;const d=new Date(date+"T12:00");OW.calM=new Date(d.getFullYear(),d.getMonth(),1);owAgenda();toast("Compromisso agendado");return}
  const ed=t.closest("[data-owevdel]");if(ed){lsj.set("sh_events",lsj.get("sh_events",[]).filter(x=>x.id!=ed.dataset.owevdel));OW.tab==="ag"?owAgenda():owHome();toast("Compromisso excluído");return}
  if(t.closest("[data-owcfgsave]")){const c=cfg(),cm=parseFloat($("#cfg-comm").value.replace(",",".")),mg=parseFloat($("#cfg-margin").value.replace(",","."));
    if(!(cm>=0&&cm<=50)||!(mg>0&&mg<100)){toast("Use comissão entre 0 e 50% e margem entre 1 e 99%");return}c.comm=cm;c.margin=mg;setCfg(c);owShell();toast("Ajustes salvos");return}
  const rs=t.closest("[data-owreset]");if(rs){if(rs.dataset.sure!=="1"){rs.dataset.sure="1";rs.textContent="Confirmar: apagar dados e restaurar exemplos";return}
    ["sh_orders","sh_seeded4","sh_seed_owner","sh_exp","sh_events","sh_tasks","sh_cfg","sh_team","sh_stock_pnz","sh_stock_lem","sh_seq_pnz","sh_seq_lem"].forEach(k=>{try{localStorage.removeItem(k)}catch(_){}});loadTeam();seedOrders();seedOwner();owShell();toast("Dados de exemplo restaurados");return}
});
document.addEventListener("change",e=>{
  const t=e.target;if($("#v-owner").hidden&&!t.closest("#ow-modal"))return;
  if(t.dataset.owgoal){const v=parseInt(t.value.replace(/\D/g,""));if(v>0){const c=cfg();c.goals[t.dataset.owgoal]=v;setCfg(c);owTeam();toast(`Meta de ${TEAM[t.dataset.owgoal].name} atualizada`)}return}
  if(t.dataset.owtask){const ts=tasks(),x=ts.find(z=>z.id==t.dataset.owtask);if(x){x.done=t.checked;setTasks(ts);owTeam()}return}
  if(t.dataset.owreassign){const v=t.value||null;updOrder(t.dataset.owreassign,o=>{o.seller=v});owOrders();toast(v?`Pedido atribuído a ${v}`:"Pedido sem atendente");return}
  if(t.id==="ow-ost"){OW.of.st=t.value;owOrders();return}
  if(t.id==="ow-osel"){OW.of.sel=t.value;owOrders();return}
});
document.addEventListener("input",e=>{
  const t=e.target;
  if(t.dataset.owpin!=null){t.value=t.value.replace(/\D/g,"").slice(0,1);const i=+t.dataset.owpin;if(t.value&&i<3)$(`[data-owpin='${i+1}']`).focus();
    const code=[...document.querySelectorAll("[data-owpin]")].map(x=>x.value).join("");
    if(code.length===4){if(code===OWNER_PIN){OW.auth=true;ls.set("sh_ow","1");OW.tab="geral";owShell();toast("Painel aberto")}else{const p=$("#owpin");p.classList.remove("bad");void p.offsetWidth;p.classList.add("bad");document.querySelectorAll("[data-owpin]").forEach(x=>x.value="");$("[data-owpin='0']").focus();toast("PIN incorreto")}}return}
  if(t.id==="ow-oq"){OW.of.q=t.value;clearTimeout(OW.t);OW.t=setTimeout(()=>{owOrders();const i=$("#ow-oq");i.focus();i.setSelectionRange(i.value.length,i.value.length)},200);return}
});
document.addEventListener("keydown",e=>{
  if(e.target.dataset?.owpin!=null&&e.key==="Backspace"&&!e.target.value){const i=+e.target.dataset.owpin;if(i>0)$(`[data-owpin='${i-1}']`).focus()}
  if(e.key==="Escape")owCloseModal();
  if(e.key==="Enter"&&e.target.id?.startsWith("nt-")){$(`[data-owtaskadd="${e.target.id.slice(3)}"]`)?.click()}
});

/* altura do bloco do header que rola para fora no celular */
function setHM(){const h=$(".h-main");if(h&&h.offsetHeight)document.documentElement.style.setProperty("--hm",h.offsetHeight+"px")}
addEventListener("resize",setHM);
if("ResizeObserver" in window)new ResizeObserver(setHM).observe($(".h-main"));

window.addEventListener("hashchange",route);
route();setHM();
