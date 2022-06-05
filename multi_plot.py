def helper(value, j):
    '''
    helper function for data_plot()
    '''
    if value == "None":
        return None
    elif type(value) == list and j <= len(value):
        return value[j]
    else: #not a list so only one value
        if j == 0:
            return value
        else:
            return None

def data_plot(data = None, x = None, y = None,
              x_title = None, y_title = None, title = None,
              **kwargs):
    '''
    list of pandas.DataFrame, list of str, list of str, list of str, kwargs -> plotly plot object

    Precondition: If an argument has multiple objects, they must be in a list (can have nested lists).
                  The order of the arguments must be in the same order as the DataFrames.
                  There must be the same number of x columns as y columns passed.

                  ex) ocv_plot(
                      data = [df1, df2],
                      x = [ df1["SOC"], df2["SOC-Dis"] ],
                      y = [ df1["OCV"], df2["OCV-Dis"] ],
                      mode = ["lines+markers", "markers"],
                      color = ["mintcream", "darkorchid"]
                      )

    ****Note:if only one DataFrame and one column for the x-axis are needed then use line_plot() instead.
             line_plot() can accept multiple columns for the y-axis.
             This function will not work well for simple plots.

    This function takes one or more DataFrames, columns from the respective DataFrames to be plot on x and y-axes.
    It also takes the mode of plotting desired for the DataFrames and optional keyword arguments.
    It outputs a plotly plot of the data from the columns that were passed.

    Parameters:
    `data` DataFrame or list of DataFrames
        Preferrable if these DataFrames are the output of generate_ocv_pts() and ocv_estimate()

    `x` columns, list of columns or nested lists of columns
        example of each option in order:
            x = "SOC-Dis"
            x = ["SOC-Dis","SOC-Chg","SOC"]
            x = [ ["Test Time (sec)","Step Time (sec)"], "Step"]
                Test Time and Step Time are both from the same DataFrame; there must be two y columns as well.

    `y` columns, list of columns or nested lists of columns
        View `x` for help

    `x_title` str
        the name of the x_axis to be displayed
        else None

    `y_title` str
        the name of the y_axis to be displayed
        else None

    `title` str
        The title of the Plot
        default None will not add a title

    **kwargs: (alphabetical order)

    `color` str, list of str, nested lists of str:
        same principle as above arguments,
        assigns the color of the individual data lines.
        if no value is passed for a plot, plotly will do it automatically.

        The 'color' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, rebeccapurple, saddlebrown, salmon,
                sandybrown, seagreen, seashell, sienna, silver,
                skyblue, slateblue, slategray, slategrey, snow,
                springgreen, steelblue, tan, teal, thistle, tomato,
                turquoise, violet, wheat, white, whitesmoke,
                yellow, yellowgreen
          - A number that will be interpreted as a color
            according to scatter.marker.colorscale
          - A list or array of any of the above

    `mode` str, list of str, nested lists of str:
        default None: will set mode = "lines"
        Note: str must be one of "lines", "markers", "lines+markers" which are self-explanatory
        example of each option in order:
            mode = "markers"
            mode = ["lines+markers", "lines"]
            mode = ["lines+markers",["lines","lines"]]

    `name` str, list of str, nested list of strs
        same principle as above arguments
        assigns the names of the individual data lines to be displayed in the legend

    `size` int/float, list of int/float or nested lists of int/float
        same principle as above arguments
        assigns the size of the individual data lines
        if no value is passed, plotly will do it automatically.


    >>>df1 = generate_ocv_pts("JMFM_12_SOC_OCV_Test_220411.txt", to_csv = False)
    >>>df2 = ocv_estimate(df1, to_csv = False)
    >>>data_plot(data = [df1,df2],
          x=[ ["SOC-Chg","SOC-Dis"],"SOC" ],
          y = [ ["OCV-Chg","OCV-Dis"], "OCV" ],
          title = "JMFM-12 OCV vs. SOC Curve",
          x_title = "SOC (%)",
          y_title = "OCV (V)",
          mode = [ ["markers","markers"] ],
          color = [ ["violet","lightcoral"], "darkorchid"],
          name = [ ["Charge-OCV","Discharge-OCV"], "OCV"],
          size = [[4.5,4.5]]
         )
    figure...
    '''

    if not pd.Series(
                    pd.Series([len(x), len(y)]) == len(data)
                    ).all():
        return '''Error: x and y columns passed much match the number of DataFrames passed
        Use nested lists for multiple columns from the same DataFrame
        '''

    if "mode" in kwargs.keys():
        if len(kwargs["mode"]) > len(data):
            return "Error: passed more modes than DataFrames"

    if "color" in kwargs.keys():
        if len(kwargs["color"]) > len(data):
            return "Error: passed more colors than DataFrames"

    if "name" in kwargs.keys():
        if len(kwargs["name"]) > len(data):
            return "Error: passed more names than DataFrames"

    if "size" in kwargs.keys():
        if len(kwargs["size"]) > len(data):
            return "Error: passed more sizes than DataFrames"

    frame = pd.DataFrame(data = {"x" : x, "y" : y})

    for i in ["color","mode","name","size"]:
        frame = frame.join(pd.Series(kwargs.get(i), name = i, dtype = "object"), how = "outer")

    frame.fillna("None",inplace=True)

    figure = make_subplots(x_title = x_title, y_title = y_title, subplot_titles = [title])

    for i in frame.index:
        if type(data) == list:
            use_data = data[i]
        else:
            use_data = data

        if type(frame["x"][i]) == list: #y[i] must be a list
            for j in range(len(x[i])):
                use_x = frame.loc[i,"x"][j]
                use_y = frame.loc[i,"y"][j]

                use_color = helper(frame.loc[i,"color"], j)
                use_mode = helper(frame.loc[i,"mode"], j)
                use_name = helper(frame.loc[i,"name"], j)
                use_size = helper(frame.loc[i,"size"], j)

                figure.add_trace(
                    go.Scatter(
                        x = use_data[use_x], y = use_data[use_y],
                        mode = use_mode, marker = {"size" : use_size, "color" : use_color},
                        name = use_name)
                    )
        else: #x[i] and y[i] are not lists
            use_x = use_x = frame.loc[i,"x"]
            use_y = frame.loc[i,"y"]
            use_color = helper(frame.loc[i,"color"], 0)
            use_mode = helper(frame.loc[i,"mode"], 0)
            use_name = helper(frame.loc[i,"name"], 0)
            use_size = helper(frame.loc[i,"size"], 0)
            #zero is just a placholder

            figure.add_trace(
                go.Scatter(
                    x = use_data[use_x], y = use_data[use_y],
                    mode = use_mode, marker = {"size" : use_size, "color" : use_color},
                    name = use_name)
                )
    return figure
