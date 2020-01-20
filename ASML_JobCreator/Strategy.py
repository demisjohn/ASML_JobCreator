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
from .Mark import Mark as __Mark      # Mark class


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
    
    def __init__(self, ID, marks=None, parent=None):
        '''
        Parameters
        ----------
        ID : string
            Name of the strategy
        
        marks : iterable
            Iterable containing Mark objects to add to this strategy.
        
        parent : Alignment object
            The Alignment object this Strategy belongs to.
        '''
        self.parent = parent    # parent Alignment object
        self.StrategyID = self.set_ID(ID)
        
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
    def add_mark ( self, marks, preference="preferred" ) :
        '''        
        Parameters
        ----------
        marks : an iterable of Mark objects, or single Mark object
            Pass the Mark objects to add to this Alignment Strategy. Accepts each Mark as a single Mark object, or an iterable containing Mark objects.
            Eg. both of the following are acceptable:
                add_mark( NorthEast_PMMark )
                add_mark( [NE_Mark, SE_Mark, S_Mark, N_Mark] )
        
        preference : {"backup", "preferred"}, optional
            Should Mark(s) be added as prefferred or backup marks? Preferred is default.
            Synonyms for "preferred" include "p", case-insensitive
            Synonyms for "backup" include "b", case-insensitive
        '''
        
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
                errstr = "Passed argument option `%s` is not in th elist of valid options, which are:\n\t" + str(PStrings) + "\n\t" +str(BStrings)
                raise ValueError(errstr)
            #end if
        #end get_markpref()
        
        if isinstance( marks, __Mark):
            self.MarkList.append( marks )
            MarkPrefList.append( get_markpref(preference)  )
        else:
            try:
                for m in marks:
                    if isinstance( m, __Mark ):
                        self.MarkList.append( m )
                    else:
                        errstr = "Expected Mark object, instead got `%s` %s." %( str(m), str(type(m)) )
                        raise ValueError(errstr)
                    MarkPrefList.append( get_markpref(preference)  )
                #end for(marks)
            except IndexError:
                errstr = "Expected an iterable or single Mark object, instead got `%s%` of type '%s'." %(  str(m), str(type(m))  )
                raise IndexError(errstr)
        #end if(isMark)
        
    #end (add_mark)
    
    
    
    
    
  
#end class(Trace)





################################################
################################################


