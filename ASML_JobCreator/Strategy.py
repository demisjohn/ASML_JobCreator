"""
This file is part of the ASML_JobCreator package for Python 3.x.

Strategy.py
    Contains Alignment Strategy options in class 'Strategy'.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.
from .Mark import Mark as _Mark      # Mark class


####################################################




class Strategy(object):
    """
    Class for defining Alignment Strategy.
    
    
    Attributes
    ----------
        parent : The parent Alignment object, that this Strategy belongs to. The Job is accessible via `parent.parent`.
        
        ID : string
            Name of the strategy
        
        marks : iterable
            Iterable containing Mark objects to add to this strategy.
        
    """
    
    def __init__(self, StrategyID, marks=None, parent=None):
        '''
        Parameters
        ----------
        StrategyID : string
            Name of the strategy
        
        marks : iterable of Mark objects, optional
            Iterable containing Mark objects to add to this strategy. Can instead add later with `add_mark()`.
        
        parent : Alignment object
            The Alignment object this Strategy belongs to.
        '''
        self.parent = parent    # parent Alignment object
        self.set_ID(StrategyID)
        
        self.MarkList = []
        self.MarkPrefList = []
        if marks:
            for m in marks:
                self.add_mark( m )
        #end if(marks)
        
        self.parent.add_Strategy(self)
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Strategy object:\n"
        
        return s
    #end __str__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Setters/Getters
    ##############################################
    
    def set_ID(self, ID):
        '''Set the Strategy ID as string.'''
        self.StrategyID = str(ID)
    #end
    
    
    def get_ID(self):
        '''Return Strategy ID as string.'''
        try:
            return self.StrategyID
        except AttributeError:
            raise AttributeError("Strategy ID has not been set yet.  Use `Strategy.set_ID()`.")
    #end
    
    
    
    
    ##############################################
    #       General Functions
    ##############################################
    def add_mark ( self, *marks, preference="preferred" ) :
        '''        
        Parameters
        ----------
        marks : a single Mark object
            Pass the Mark objects to add to this Alignment Strategy. Accepts each Mark as a single Mark object, or an iterable containing Mark objects.
            Eg. both of the following are acceptable:
                add_mark( NorthEast_PMMark )
                add_mark( [NE_Mark, SE_Mark, S_Mark, N_Mark] )
        
        preference : {"backup", "preferred"}, optional
            Should Mark(s) be added as prefferred or backup marks? Preferred is default.
            Synonyms for "preferred" include "p", case-insensitive
            Synonyms for "backup" include "b", case-insensitive
        '''
        
        ### Internal funcs ###
        def get_markpref( s ):
            '''Analyze string argument `s` and Return 'p' for preferred mark, 'b' for backup mark'''
            # argument synonym options:
            PStrings = ["preferred","p"]
            BStrings = ["backup","b"]
            
            s = str(s).strip().lower()
            if np.any(  np.isin( PStrings , s )  ):
                return 'p'
            elif np.any(  np.isin( BStrings , s )  ):
                return 'b'
            else:
                errstr = "Passed argument option `%s` is not in the list of valid options, which are:\n\t" + \
                    str(PStrings) + "\n\t" + \
                    str(BStrings)
                raise ValueError(errstr)
            #end if
        #end get_markpref()
        
        ## Add the Marks
        for i,m in enumerate(marks):
            if isinstance(m, _Mark):
                if not np.isin( m, self.parent.MarkList ):
                    raise ValueError(   "Strategy.add_mark(): Mark %s not found in parent Job %s. Can't add to Strategy."%(m.__repr__, self.parent.__repr__)   )
                #end isin(Mark)
                
                if np.isin( m, self.MarkList ):
                    raise ValueError(   "Strategy.add_mark(): Mark %s is already in this Strategy, can not add again."%(m.__repr__)   )
                    
                self.MarkList.append( m )
                self.MarkPrefList.append( get_markpref(preference)  )
            else:
                raise ValueError( "Expected `Mark` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(marks)
    #end (add_mark)
    
    
    def set_required_marks(self, num):
        '''Set the minimum number of marks required to pass during Mark measurement.'''
        self.required_marks = num
    #end set_required_marks()
    
    def get_required_marks(self, num):
        '''Return the number of required marks to pass during Mark measurement.'''
        return self.required_marks
    #end get_required_marks()

    
  
#end class(Trace)





################################################
################################################


