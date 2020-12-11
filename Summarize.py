import inspect

def SummarizeConnections(obj):
    print('\n%s' % obj.Name)
    PrintSourceConnections(obj)
    PrintDestinationConnections(obj)
    PrintConnections('Owned', obj.GetOwnedCount, obj.GetOwned)

def PrintConnections(name, countFunc, getFunc):
    '''
    Prints an indexed list of the connections for a particular component.
    @param name: The type of connection to be printed, typically 'Source'
        or 'Destination'.
    @param countFunc: GetSrcCount or GetDstCount.
    @param getFunc: GetSrc or GetDst.
    '''
    n = countFunc()
    print('\n%s connections (%d):\n----------' % (name, n))

    for i in range(0, n):

        current = getFunc(i)
        try:
            print('[%d]: %s %s' % (i, current.LongName, current))
        except AttributeError:
            print('[%d]: %s' % (i, current))

def PrintSourceConnections(obj):
    '''
    Prints an indexed list of the source connections for this component.
    '''
    PrintConnections('Source', obj.GetSrcCount, obj.GetSrc)

def PrintDestinationConnections(obj):
    '''
    Prints an indexed list of the destination connections for this component.
    '''
    PrintConnections('Destination', obj.GetDstCount, obj.GetDst)

def PrintMethods(obj, methodList):
    '''
    Prints a list of method names for the given object. Expects to be
    given an already-compiled list of method names.
    '''
    print('\nMethods (%d):\n----------' % len(methodList))
    for methodName in methodList:
        print(methodName)

def PrintProperties(obj, propertyList):
    '''
    Prints a list of property names, along with the current value for
    each property, for the given object. Expects to be given an
    already-compiled list of property names.
    '''
    print('\nProperties (%d):\n----------' % len(propertyList))
    for propertyName in propertyList:
        print('%s: %s' % (propertyName, obj.__getattribute__(propertyName)))

def Summarize(obj, searchText = ''):
    '''
    Prints a summary of the given object, which should be an instance
    of an FBComponent subclass. searchText may be optionally specified
    in order to filter the methods and properties grep-style.
    '''
    searchText = searchText.lower()
    methods = []
    properties = []

    for prop in [p for p in dir(obj) if not p.startswith('_')]:

        if searchText and prop.lower().find(searchText) < 0:
            continue

        if inspect.ismethod(obj.__getattribute__(prop)):
            methods.append(prop)
        else:
            properties.append(prop)

    try:
        print('%s\n%s' % (obj.LongName, obj))
    except AttributeError:
        print(obj)

    PrintSourceConnections(obj)
    PrintDestinationConnections(obj)
    PrintMethods(obj, methods)
    PrintProperties(obj, properties)