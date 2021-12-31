import pandas as pd
import plotly.express as px

class Data():

	def get_data(self):
		return px.data.gapminder()

	def process_data(self):

		# load data
		df = Data().get_data()

		# rename
		df = df.rename(columns=dict(lifeExp="cars", pop="euro", gdpPercap="units", continent="region"))

		# reshape
		id_vars = ["country", "region", "year"]
		value_vars = ["cars", "euro", "units"]
		df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name="unit")

		# add world
		df2 = df.groupby(["year", "unit"]).value.sum().reset_index()
		df2["region"] = "World"
		df2["country"] = ""
		return df.append(df2)
