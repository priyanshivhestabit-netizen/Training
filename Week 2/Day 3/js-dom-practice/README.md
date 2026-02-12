# Day 3 - JavaScript ES6 + DOM Manipulation 

## Objective
The goal of this task was to understand and implement **modern JavaScript (ES6)** concepts and practice **DOM manipulation** by building an interactive FAQ accordion component without using any frameworks.

The focus was on handling user interactions dynamically using event listeners and modifying the DOM structure in real time.


## What I built
I created an interactive **FAQ Accordion component** consisting of:

- Four accordion items
- Clickable headers
- Expandable and collapsible content sections
- Dynamic + / − toggle icons
- Styled UI with shadows and circular icons

The accordion supports:
- Opening and closing sections on click
- Dynamic class toggling for state management


## What I learned

### 1 - ES6 Concepts

Used modern JavaScript features including:

- const and let
- Arrow functions (() => {})
- forEach() iteration
- classList methods
- querySelector() and querySelectorAll()



### 2 - DOM Manipulation

Practiced:

- Selecting DOM elements
- Adding event listeners
- Traversing parent elements
- Dynamically adding and removing classes
- Updating text inside elements

Key methods used:

- document.querySelectorAll()
- addEventListener()
- parentElement
- classList.add()
- classList.remove()
- classList.toggle()
- textContent


### 3 - State Management Concept

Implemented two behavioral approaches:

#### Single Open Section
- Clicking one section closes others
- Achieved by looping through all accordion items and removing the active class

![single_open](/Day%203/images/one_open.png)

#### Multiple Open Sections
- Each section toggles independently
- Only the clicked element’s state changes

![multiple_open](/Day%203/images/multi_open.png)
This helped in understanding how UI state is controlled using classes.


### 4 - CSS & JavaScript Interaction

Learned how:

- JavaScript modifies class names
- CSS reacts to those classes
- The browser recalculates layout (reflow)
- The browser repaints updated elements

Example:

```css
.accordian-item.active .accordian-c {
    display: block;
}
```

JavaScript controls behavior.  
CSS controls appearance.


### 5 - UI Enhancements

Added:

- Box shadows for depth
- Circular icon styling using border-radius
- Flexbox for centering icons

Example:

```css
.icon {
    width: 30px;
    height: 30px;
    background: white;
    color: rgb(98, 125, 234);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
```


## Files Used

- index.html - Structure of the accordion component
- style.css - Styling, layout, shadows, transitions
- script.js - ES6 logic and DOM manipulation


## Output

The final output is a fully interactive FAQ accordion component that:

- Expands and collapses dynamically
- Updates icon states in real time
- Uses modern JavaScript syntax without frameworks

