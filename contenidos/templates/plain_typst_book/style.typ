  
#let leftCaption(it) = {
  set text(size: 8pt)
  set align(left)
  set par(justify: true)

  // Within the context of the element, you may use the counter
  context(it, {
    text(weight: "bold")[#it.supplement #it.counter.display(it.numbering).]
  })

  h(4pt)
  set text(fill: black.lighten(20%), style: "italic")
  it.body
}


#let template(
  // FRONTPAGE.
  title: "Apunte Estructuras de Datos",
  subtitle: "Ingeniería en Computación",
  authors: "Cátedra de Estructuras de Datos",
  cover: "untref-logo.svg",            // <— path to cover "images/cover.png"
  cover_width: 12cm,    
  coverposition: 1cm,
  justification: false,

  // TOC
  ToC_depth: 2,
  show_ToC: true,

  // PREFACE
  preface: none,

  // SPECIFICATION of output
  paper-size: "a4",       // https://typst.app/docs/reference/layout/page/#parameters-paper
  margin: (),                          
  linespacing: .5em,
  show_pagenumber: true,
  margin_top: 2cm,
  margin_bottom: 2cm,
  margin_left: 20%,
  margin_right: 10%,
  logo: none,
  logo_width: 10%,
  
  font: ("New Computer Modern", "Noto Color Emoji"), 
  fontsize: 10pt,

  theme: blue.darken(30%),
  colorheadings: blue.darken(30%),
  
  // The book's content.
  body
) = {

  set page(
    numbering: none,
    paper-size,
    ) //numbering off until first chapter
  
  set heading(numbering: (..args) => {
    let nums = args.pos()
    let level = nums.len()
    if level == 1 {[#numbering("1.", ..nums)]} else {[#numbering("1.1.1", ..nums)]}
    },   
    
)

  // Set figure numbering to x.y where x is chapter number and y is figure number within chapter

  set figure(numbering: (..args) => {
    // get current chapter number (first level of heading)
    let chapter = counter(heading).display((..nums) => nums.pos().at(0)) // nums is array of all levels, at(0) is first level, display formats it.  
    let fig = counter(figure).display("1")    // counter counts, display formats it
    [#chapter.#fig]
  })
  

  // Configure equation numbering and spacing.
  set math.equation(numbering: (..args) => {
    let chapter = counter(heading).display((..nums) => nums.pos().at(0))
    [(#chapter.#numbering("1)", ..args.pos())]
  })
  show math.equation: set block(spacing: 1em)


  // Configure lists.
  set enum(indent: 10pt, body-indent: 9pt)
  set list(indent: 10pt, body-indent: 9pt)



// COVERPAGE
  // Title, subtitle, 
  align(center, text(17pt, weight: "bold", fill: theme, title))
  if subtitle != none {
    parbreak()
    align(center, text(14pt, fill: gray.darken(30%), subtitle))
  }

    if cover != none {
      v(coverposition)
      align(center, image((cover), width: cover_width))
    }

  //author
  v(1em)

  // authors in gray
  if authors != none {
  place(bottom + right, 
    text(12pt, fill: gray.darken(50%), authors)
  )

  }


// PREFACE, 
  if preface != none {
    pagebreak()
    place(top + left, 
      text(14pt, fill: theme, "Prefacio")
    )
    v(1em)
    set par(justify: true)
    align(center, box(width: 70%, text(11pt, overhang: true, font:  "New Computer Modern", fill: gray.darken(30%), preface)))
  }


//OUTLINE OF THE BOOK
  pagebreak()
  if show_ToC == true {
      
    show outline.entry.where(level: 1): it => {
      v(12pt, weak: true)
      
      strong(it)
    }
    // setting outline in themecolor
    outline(
    title: strong(text(fill: theme, "Índice")),
    depth: ToC_depth,
    indent: auto,
  )

  }

//RESETING NUMBERING
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    // Reset all counters with a new chapter
    counter(figure).update(0)                // all figures (irrespective of kind)
    counter(figure.where(kind: table)).update(0) // specific for tables
    counter(math.equation).update(0)
    
    set align(center + horizon)
    set text(size: 24pt)
    it
    pagebreak()
  }

  show heading.where(level: 2): it => {
    set align(center)
    set text(size: 18pt)
    block(it)
    v(1em)
  }

  //Heading colors
  show heading: set text(colorheadings)
  

// PAGE LAY OUT OF CONTENT
  set page(
    numbering: if show_pagenumber == true {"1"} else {none},         //turn on numbering
    footer: context [
      #set align(right)
      #if show_pagenumber {
        [Página #counter(page).display("1") de #counter(page).final().last()]
      }
    ],
    margin: (
      top: margin_top,
      bottom: margin_bottom,
      left: margin_left,
      right: margin_right 
      ),    //set left margin
    header: if logo != none { align(center)[#image(logo, width: logo_width)] } else { none },//include logo
  )   

  set text(
    font: font,
    size: fontsize
    )
  set par(
    leading: linespacing,
    justify: justification
    )

  counter(page).update(1)   //set number to 1

  // Display the book's contents.
  // Code block styling
  show raw.where(block: true): it => {
    let lang = if it.has("lang") { it.lang } else { none }
    let title = if lang != none {
      if lang == "python" { "Python" }
      else if lang == "rust" { "Rust" }
      else if lang == "cpp" { "C++" }
      else if lang == "c" { "C" }
      else if lang == "java" { "Java" }
      else if lang == "js" or lang == "javascript" { "JavaScript" }
      else if lang == "ts" or lang == "typescript" { "TypeScript" }
      else if lang == "html" { "HTML" }
      else if lang == "css" { "CSS" }
      else if lang == "sql" { "SQL" }
      else if lang == "bash" or lang == "sh" { "Shell" }
      else if lang == "json" { "JSON" }
      else if lang == "yaml" or lang == "yml" { "YAML" }
      else if lang == "xml" { "XML" }
      else if lang == "typ" or lang == "typst" { "Typst" }
      else { lang }
    } else { none }

    block(
      fill: luma(240),
      inset: 0pt,
      radius: 4pt,
      stroke: 0.5pt + luma(200),
      width: 100%,
      clip: true,
      {
        if title != none {
            block(
                fill: luma(220),
                width: 100%,
                inset: 8pt,
                stroke: (bottom: 0.5pt + luma(200)),
                text(weight: "bold", font: "New Computer Modern", size: 10pt, title)
            )
        }
        block(
            inset: 8pt,
            width: 100%,
            text(font: "DejaVu Sans Mono", size: 8pt, it)
        )
      }
    )
  }

  [#body]
}
