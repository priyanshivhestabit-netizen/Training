# UI Component Documentation

This document describes all reusable UI components used in the **UI Dashboard Project**, including their purpose, props, and usage.

---

## 1. Badge Component

### Purpose
Used to display small status indicators such as **Online / Offline**, **Active / Inactive**, etc.

### File Location

/components/ui/Badge.jsx


### Props
| Prop | Type | Description |
|---|---|---|
| `children` | ReactNode | Text inside the badge |
| `color` | string | Badge color (`gray`, `green`, `blue`, `red`, `yellow`) |

### Example Usage
```jsx
<Badge color="green">Online</Badge>
<Badge color="gray">Offline</Badge>
```

## 2. Button Component

### Purpose

Reusable button component with multiple variants and sizes.

### File Location

/components/ui/Button.jsx

### Props
| Prop | Type  | Description |
|---|---|
children	ReactNode	Button label
variant	string	primary, secondary, danger, outline
size	string	sm, md, lg
className	string	Additional Tailwind classes
...props	object	Native button props
Variants

Primary: Teal CTA

Secondary: Neutral background

Danger: Red action

Outline: Minimal bordered button

### Example Usage

```jsx
<Button variant="primary">Save</Button>
<Button variant="danger" size="sm">Delete</Button>
```
## 3. Card Component
### Purpose

Wraps content inside a clean container with soft shadows and padding.

### File Location
/components/ui/Card.jsx
Props
Prop	Type	Description
title	string	Optional card title
children	ReactNode	Card content
className	string	Custom styling

### Example Usage
```jsx
<Card title="Profile Info">
  <p>User details go here</p>
</Card>
```
## 4. Input Component
### Purpose

Standardized input field with optional label and focus styles.

### File Location
/components/ui/Input.jsx

### Props
Prop	Type	Description
label	string	Input label
className	string	Extra styles
...props	object	Native input props

### Example Usage
```jsx
<Input label="Email" type="email" placeholder="Enter email" />
```

## 5. Modal Component
### Purpose

Displays content in a focused overlay above the page.
Used for editing, confirmations, and forms without navigation.

### File Location
/components/ui/Modal.jsx

### Props
Prop	Type	Description
open	boolean	Controls modal visibility
onClose	function	Closes the modal
title	string	Modal heading
children	ReactNode	Modal content

### Example Usage
```jsx
<Modal open={isOpen} onClose={() => setIsOpen(false)} title="Edit User">
  <p>Edit form goes here</p>
</Modal>
```
## 6. Navbar Component
### Purpose

Top navigation bar used across dashboard pages.

### File Location
/components/ui/Navbar.jsx

Features:

- Page title

- Search input

- CTA button (Sign In)

- Uses reusable Button component

- Clean, minimal layout

## 7. Sidebar Component
### Purpose

Primary dashboard navigation that stays persistent across routes.

### File Location
/components/ui/Sidebar.jsx
Navigation Includes:

- Homepage
- Dashboard
- Users
- Billing
- Profile
- Sign In / Sign Up

## Design Rules

- Fixed width

- Full height

- Soft shadow

- Hover feedback

## Design Principles Followed

- Reusable components

- Consistent spacing & typography

- Minimal UI with soft shadows

- Tailwind utility-first approach

- Responsive-ready components

## Lessons Learned

- Component abstraction improves maintainability

- Variants reduce duplicate styles

- Modals improve UX by avoiding page navigation

- Reusability speeds up feature development