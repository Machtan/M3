# coding: utf-8
# Created by Jakob Lautrup Nysom @ March 23rd 2014
import pygame

class MouseState:
    def __init__(self, pressed, startpos, dragging):
        self.pressed = pressed
        self.startpos = startpos
        self.dragging = dragging
    
    def __getitem__(self, item):
        if item == 0: 
            return self.pressed
        elif item == 1: 
            return self.startpos
        elif item == 2: 
            return self.dragging
        else:
            raise IndexError("State member index out of range")

class MouseListener:
    """Mix-in for letting a component listen to mouse events ;)"""
    def __init__(self):
        self._mouse_state = {} # (pressed, startpos, dragging)
        self._hovered = False
    
    @property
    def _dragging(self):
        for state in self._mouse_state.values():
            if state.dragging:
                return True
        return False
    
    _members = lambda: [mem for mem in dir(MouseListener) if not mem.startswith("_")]
    
    # ------------------- Movement -------------------
    def on_mouse_moved(self, pos, rel):
        """Called when the mouse is moved"""
    
    # -------------------- Hover ---------------------
    def on_hover_enter(self, pos):
        """Called when the mouse enters this object"""
    
    def on_hover_leave(self, pos):
        """Called when the mouse leaves this object"""
    
    # -------------------- Drag ----------------------
    def on_drag_start(self, pos, button):
        """Called when the user starts dragging inside this object"""
    
    def on_drag(self, pos, rel, button):
        """Called when the user drags the mouse while a button is held"""
    
    def on_drag_end(self, pos, button):
        """Called when the user stops dragging"""
    
    # ------------ Dropping an object here -----------
    def on_drop(self, pos):
        """Called when the user stops dragging inside this object"""
    
    # -------------------- Click ---------------------
    def on_press(self, pos, button):
        """Called when the user presses a mouse button inside this object"""
    
    def on_click(self, pos, button):
        """Called when a mouse button is pressed and released without moving"""
    
    # -------------------- Scroll --------------------
    def on_scroll(self, pos, rel):
        """Called when the mouse wheel is scrolled inside this object.
        The value is -1 if the user wants the content to go up, and 1 if
        they want it to go down. (scrollwise)"""
    
    # ------------------- General --------------------
    def handle_mouse(self, event):
        """Handles and dispenses mouse input the right methods.
        Do Not Override."""
        if event.type == pygame.MOUSEMOTION:
            self.on_mouse_moved(event.pos, event.rel)
            
            if self.rect.collidepoint(event.pos): # Inside
                if self._hovered == False:
                    self.on_hover_enter(event.pos)
                    self._hovered = True
                for button, state in self._mouse_state.items():
                    if self.rect.collidepoint(state.startpos):
                        if state.pressed and not state.dragging:
                            state.dragging = True
                            self.on_drag_start(state.startpos, button)
            else: # Outside
                if self._hovered and not self._dragging:
                    self.on_hover_leave(event.pos)
                    self._hovered = False
                    
            # Drag irregardless
            for button, state in self._mouse_state.items():
                if state.pressed and state.dragging:
                    self.on_drag(event.pos, event.rel, button)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            inside = self.rect.collidepoint(event.pos)
            self._mouse_state[event.button] = MouseState(True, event.pos, False)
            if inside: # Start dragging
                if event.button in {4, 5}:
                    self.on_scroll(event.pos, -1 if event.button is 5 else 1)
                else:
                    self.on_press(event.pos, event.button)
        
        if event.type == pygame.MOUSEBUTTONUP:
            button = event.button
            if button in self._mouse_state:
                state = self._mouse_state[button]
                if state.pressed: 
                    if event.pos == state.startpos and self.rect.collidepoint(event.pos):
                        self.on_click(event.pos, event.button)
                    elif state.dragging:
                        self.on_drag_end(event.pos, button)
                    self.on_drop(event.pos) # Drop either way
                        
            self._mouse_state[button] = MouseState(False, event.pos, False)